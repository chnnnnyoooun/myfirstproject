import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.title("전 세계 시가총액 TOP 10 기업 - 지난 3년간 시가총액 변화")

# TOP 10 기업과 티커
companies = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Saudi Aramco": "2222.SR",
    "Amazon": "AMZN",
    "Alphabet": "GOOGL",
    "NVIDIA": "NVDA",
    "Tesla": "TSLA",
    "Berkshire Hathaway": "BRK-B",
    "Meta Platforms": "META",
    "Taiwan Semiconductor": "TSM"
}

# 3년 전 날짜
end_date = datetime.today()
start_date = end_date - timedelta(days=365*3)

@st.cache_data
def get_market_caps(ticker):
    # 주가와 발행주식수로 시가총액 계산
    df = yf.Ticker(ticker).history(start=start_date, end=end_date)
    df = df.reset_index()
    # 발행주식수 가져오기 (요청할 때 값이 없으면 최신 값으로 대체)
    info = yf.Ticker(ticker).info
    shares_outstanding = info.get('sharesOutstanding', None)
    if shares_outstanding is None:
        shares_outstanding = 1  # 안전장치
    df['Market Cap'] = df['Close'] * shares_outstanding
    return df[['Date', 'Market Cap']]

# 데이터 불러오기 및 병합
market_caps = {}
for name, ticker in companies.items():
    with st.spinner(f"{name} 데이터 불러오는 중..."):
        df = get_market_caps(ticker)
        market_caps[name] = df

# Plotly figure 생성
fig = go.Figure()
for company, df in market_caps.items():
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Market Cap'] / 1e9,  # 단위: 십억 달러
                             mode='lines',
                             name=company))

fig.update_layout(
    title="지난 3년간 시가총액 변화 (단위: 십억 달러)",
    xaxis_title="날짜",
    yaxis_title="시가총액 (십억 달러)",
    hovermode='x unified'
)

st.plotly_chart(fig, use_container_width=True)
