import streamlit as  st
from  client import API_STOCK_MARKET
 
##  give  page  title
st.set_page_config(page_title  = 'Stock  Market  App  deployment' ,  layout= 'wide')
 
## add  title  inside page
st.title("Stock  market  candelstick  chart ploting  ")
 
st.subheader("By Vaishnavi  Rayphale")
 
 
company_name  =  st.text_input("Company Name")
 
##  create  function to fetch data
 
@st.cache_resource(ttl=3600)
def fetch_data():
    return  API_STOCK_MARKET(st.secrets["API_KEY"])
 
stock_api =  fetch_data()
 
## search symbol
@st.cache_data(ttl  =  3600)
def get_symbol(company):
    return stock_api.search_symbol(company)
 
## create  function to  fetch time series data
@st.cache_data(ttl =  3600)
def Time_series_data(symbol):
    return stock_api.time_series_daily(symbol)
 
 
# create  function  for plot
@st.cache_data(ttl =  3600)
def plot_chart(symbol):
    return stock_api.plot(symbol)
 
if company_name :
    company_data  = get_symbol(company=company_name)
 
    if  company_data:
        symbol_list  = list(company_data.keys())
        option  =  st.selectbox("Symbol" ,  symbol_list)
 
        COMPNAY_NAME =  st.success(f"**COMPANY_NAME**: , {company_data[option][0]}")
        COMPNAY_REGION =  st.success(f"**COMPANY_region**: , {company_data[option][1]}")
        COMPNAY_currency =  st.success(f"**COMPANY_currency**: , {company_data[option][2]}")
 
 
     # add  button
   
    submit  = st.button('plot' ,  type  ='primary')
 
 
        # plot the graph
 
    if  submit:
        graph  = plot_chart(option)
 
        st.plotly_chart(graph)
       
       
       
 
 
 
 
 