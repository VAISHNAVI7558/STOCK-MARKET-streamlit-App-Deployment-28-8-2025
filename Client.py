import pandas as  pd
import requests
import plotly.graph_objects as  go

## create  class
class API_STOCK_MARKET:
    def __init__(self , api_key   ):
        self.api_key  =  api_key
        self.headers  =  {
                     "x-rapidapi-key": self.api_key,
                     "x-rapidapi-host": "alpha-vantage.p.rapidapi.com"  }
        self.url  =   "https://alpha-vantage.p.rapidapi.com/query"
 
 
    # extract  symbols  
    def  search_symbol(self ,  keyword):
        querystring = {"datatype":"json",
                       "keywords":keyword,
                       "function":"SYMBOL_SEARCH"}
        response = requests.get(self.url, headers=self.headers, params=querystring)
 
        data  =  response.json()
        data1  =  {}
        for  i  in data['bestMatches']:
            symbol  =  i['1. symbol']
            data1[symbol] =  [i['2. name'], i['4. region'] , i['8. currency']]
        return  data1
 
     ## fetch time series daily
    def  time_series_daily(self  ,  symbol):
        querystring = {"function":"TIME_SERIES_DAILY",
                       "symbol":symbol,
                       "outputsize":"compact",
                       "datatype":"json"}
 
        response = requests.get(self.url,
                                headers=self.headers,
                                 params=querystring)
 
        data2 =  response.json()
        # convert  in dataframe
        df  = pd.DataFrame(data2['Time Series (Daily)']).T
        # change data type  of columns
        df['1. open'] =  pd.to_numeric(df['1. open'])
        df['4. close'] = pd.to_numeric(df['4. close'])
        df['2. high'] = pd.to_numeric(df['2. high'])
        df['3. low'] = pd.to_numeric(df['3. low'])
        # change  data type  of index
        df.index  =  pd.to_datetime(df.index)
        # give name to index
        df.index.name  = 'Date'
        return  df
   
   
    #  plot  graph
    def plot(self, symbol ):
        df  =  self.time_series_daily(symbol)
        fig = go.Figure(data=[go.Candlestick(x=df.index,
                open=df['1. open'],
                high=df['2. high'],
                low=df['3. low'],
                close=df['4. close'])])
 
        fig.update_layout(title ='candelstick Chart' ,
                          xaxis_title = 'date' ,
                            yaxis_title = 'Price')
        return  fig