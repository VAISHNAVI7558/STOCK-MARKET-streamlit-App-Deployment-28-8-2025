import streamlit as st
from Client import API_STOCK_MARKET

# Page config
st.set_page_config(page_title='Stock Market App Deployment', layout='wide')

# Titles
st.title("Stock Market Candlestick Chart Plotting")
st.subheader("By Vaishnavi Rayphale")

# User input
company_name = st.text_input("Company Name")

# Create API object (cache resource)
@st.cache_resource(ttl=3600)
def fetch_data():
    return API_STOCK_MARKET(st.secrets["API_KEY"])

stock_api = fetch_data()

# Search symbol
@st.cache_data(ttl=3600)
def get_symbol(company):
    return stock_api.search_symbol(company)

# Fetch time series data
@st.cache_data(ttl=3600)
def time_series_data(symbol):
    return stock_api.time_series_daily(symbol)

# Plot chart
@st.cache_data(ttl=3600)
def plot_chart(symbol):
    return stock_api.plot(symbol)

# Main logic
if company_name:
    company_data = get_symbol(company=company_name)

    if company_data:
        symbol_list = list(company_data.keys())
        option = st.selectbox("Symbol", symbol_list)

        # Display company info
        st.success(f"**COMPANY NAME**: {company_data[option][0]}")
        st.success(f"**COMPANY REGION**: {company_data[option][1]}")
        st.success(f"**COMPANY CURRENCY**: {company_data[option][2]}")

        # Button for plotting
        submit = st.button('Plot', type='primary')

        if submit:
            graph = plot_chart(option)
            st.plotly_chart(graph)
