import streamlit as st
#import pandas as pd
from datetime import datetime, timedelta
#import yfinance as yf
import investpy as ip
import plotly.graph_objs as go
import pandas_datareader.data as web



countries = ['Brazil', 'United States']
intervals = ['Daily', 'Weekly', 'Monthly']
start_date = datetime.today()-timedelta(days=30)
end_date = datetime.today()

@st.cache
#def consultar_acao(stock, country, from_date, to_date, interval):
#    df = web.DataReader(stock=stock +'.SA',
#                     country=country,
#                     from_date=from_date,
#                     to_date=to_date,
#                     interval=interval)
#    return df

def consultar_acao(name, data_source, start, end):
    df = web.DataReader(name=name,
                        data_source=data_source,
                        start=start,
                        end=end)
    return df


def format_date(dt, format='%d/%m/%Y'):
    return dt.strftime(format)

def plotCandleStick(df, acao='ticket'):
    trace1 = {
        'x': df.index,
        'open': df.Open,
        'close': df.Close,
        'high': df.High,
        'low': df.Low,
        'type': 'candlestick',
        'name': acao,
        'showlegend': False
    }
    data = [trace1]
    layout = go.Layout()

    fig = go.Figure(data=data, layout=layout)
    return fig

## BARRA LATERAL
barra_lateral = st.sidebar.empty()

country_select = st.sidebar.selectbox('País', countries)

acoes = ip.get_stocks_list(country=country_select)
SA = '.SA'
acoesbr = [x + SA for x in acoes]

stock_select = st.sidebar.selectbox('Ativo', acoesbr)


from_date = st.sidebar.date_input('De:', start_date)
to_date = st.sidebar.date_input("Para:", end_date)

interval_select = st.sidebar.selectbox('Seleciona o Intervalo', intervals)

carregar_dados = st.sidebar.checkbox('Carregar dados')

## ELEMENTOS CENTRAIS DA PAGINA

st.title('Stock Monitor')

st.header('Ações')

st.subheader('Gráfico')

## GRAFICOS

grafico_candle = st.empty()
grafico_line = st.empty()

if from_date > to_date:
    st.sidebar.error('Data de início maior do que a data final')
else:
    df = consultar_acao(stock_select, 'yahoo', format_date(from_date), format_date(to_date))
    try:
            fig = plotCandleStick(df)
            grafico_candle = st.plotly_chart(fig)
            grafico_line = st.line_chart(df.Close)

            if carregar_dados:
                st.subheader('Dados')
                dados = st.dataframe(df)
    except Exception as e:
        st.error(e)






st.write()
