#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
pio.templates.default = 'plotly_white'


# In[2]:


stock_data = pd.read_csv('stocks.csv')


# In[3]:


stock_data.sample(10)


# # Descriptive statistics

# In[4]:


desc_stats = stock_data.groupby('Ticker')['Close'].describe().T
desc_stats


# # Time Series Analysis

# In[5]:


stock_data['Date'] = pd.to_datetime(stock_data['Date'])
pivot_data = stock_data.pivot(index='Date', columns='Ticker', values='Close')
pivot_data

#create a subplot
fig = make_subplots(rows=1, cols=1)
for column in pivot_data.columns:
    fig.add_trace(go.Scatter(x=pivot_data.index, y=pivot_data[column], name=column),row=1, col=1)

fig.update_layout(
    title_text = 'Time series of closing prices',
    xaxis_title = 'Date',
    yaxis_title = 'Closing Price',
    legend_title = 'Ticker',
    showlegend = True
)

fig.show()


# # Volatility Analysis

# In[6]:


volatility = pivot_data.std().sort_values(ascending=False)

fig = px.bar(volatility, x=volatility.index, y=volatility.values,
            labels ={'y' : 'Standard Deviation', 'x' : 'Ticker'},
            title='Volatility of Closing Prices(Standard Deviation)')

fig.show()


# # Correlation Analysis

# In[7]:


corr_matrix = pivot_data.corr()

fig = go.Figure(data = go.Heatmap(
    z= corr_matrix, 
    x= corr_matrix.columns,
    y= corr_matrix.columns,
    colorscale='Viridis',
    colorbar=dict(title='Correlation')))
fig.update_layout(
    title='Correlation Matrix of CLosing Prices',
    xaxis_title='Ticker',
    yaxis_title='Ticker'
)
fig.show()


# # Comparative Analysis

# In[8]:


#calculating percentage change 
percentage_change = ((pivot_data.iloc[-1] - pivot_data.iloc[0])/pivot_data.iloc[0])*100

fig = px.bar(percentage_change,
            x=percentage_change.index,
            y=percentage_change.values)
fig.update_layout(title='Percent change in Closing Prices',
                 xaxis_title='Ticker',
                 yaxis_title ='Percent Change(%)')
fig.show()


# # Daily Risk Vs. Return Analysis

# In[9]:


daily_returns = pivot_data.pct_change().dropna()
avg_daily_returns = daily_returns.mean()
risk = daily_returns.std()
risk_return_df = pd.DataFrame({'Risk' : risk, 'Average Daily Return' : avg_daily_returns})

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=risk_return_df['Risk'],
    y=risk_return_df['Average Daily Return'],
    mode='markers+text',
    text=risk_return_df.index,
    textposition='top center',
    marker=dict(size=10)
))
fig.update_layout(
    title='Risk vs. Return Analysis',
     xaxis_title='Risk (Standard Deviation)',
     yaxis_title='Average Daily Return',
     showlegend=False)
fig.show()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




