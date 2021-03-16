import streamlit as st
import requests
import config
from iex import IEXStock
from helpers import format_number
from datetime import datetime, timedelta

symbol = st.sidebar.text_input("Symbol", value="MSFT")
stock = IEXStock(config.IEX_TOKEN, symbol)

screen = st.sidebar.selectbox("View", ('Overview','Fundamentals','News','Ownership','Technicals'))

st.title(screen)

base_url = "https://cloud.iexapis.com/stable"
if screen == 'Overview':
    logo = stock.get_logo()
    company_info = stock.get_company_info()

    col1, col2 = st.beta_columns([1,11])

    with col1:
        st.image(logo['url'])

    with col2:
        st.subheader(company_info['companyName'])
        st.subheader('Description')
        st.write(company_info['description'])
        st.subheader('Industry')
        st.write(company_info['industry'])
        st.subheader('CEO')
        st.write(company_info['CEO'])
    
if screen == 'Fundamentals':
    stats = stock.get_stats()
    st.header('Ratios')

    col1, col2 = st.beta_columns(2)

    with col1:
        st.subheader('P/E')
        st.write(stats['peRatio'])
        st.subheader('Forward P/E')
        st.write(stats['forwardPERatio'])
        st.subheader('PEG Ratio')
        st.write(stats['pegRatio'])
        st.subheader('Price to Sales')
        st.write(stats['priceToSales'])
        st.subheader('Price to Book')
        st.write(stats['priceToBook'])
    with col2:
        st.subheader('Revenue')
        st.write(format_number(stats['revenue']))
        st.subheader('Cash')
        st.write(format_number(stats['totalCash']))
        st.subheader('Debt')
        st.write(format_number(stats['currentDebt']))
        st.subheader('200 Day Moving Average')
        st.write(stats['day200MovingAvg'])
        st.subheader('50 Day Moving Average')
        st.write(stats['day50MovingAvg'])



if screen == 'News':
    news = stock.get_company_news()

    for article in news:
        st.subheader(article['headline'])
        dt = datetime.utcfromtimestamp(article['datetime']/1000).isoformat()
        st.write(f"Posted by {article['source']} at {dt}")
        st.write(article['url'])
        st.write(article['summary'])
        st.image(article['image'])

if screen == 'Ownership':
    st.subheader("Institutional Ownership")
    
    institutional_ownership = stock.get_institutional_ownership()

    for institution in institutional_ownership:
        st.write(institution['date'])
        st.write(institution['entityProperName'])
        st.write(institution['reportedHolding'])

    st.subheader("Insider Transactions")

    insider_transactions = stock.get_insider_transactions()
    
    for transaction in insider_transactions:
        st.write(transaction['filingDate'])
        st.write(transaction['fullName'])
        st.write(transaction['transactionShares'])
        st.write(transaction['transactionPrice'])

if screen == 'Technicals':
    pass
