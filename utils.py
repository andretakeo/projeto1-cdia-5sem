from flask import Flask
from flask import request,Response
import sqlite3
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np





def getAll():
    conn = sqlite3.connect('stock.db')
    strSQL="SELECT Symbol, Date_Time, Open, High, Low, Close, Volume, Dividends, Stock_Splits, Return, Acc_Return FROM stock"
    df = pd.read_sql(strSQL, conn)
    conn.close()
    return df

def showSymbols():
    conn = sqlite3.connect('stock.db')
    strSQL="SELECT DISTINCT Symbol FROM stock"
    df = pd.read_sql(strSQL, conn)
    conn.close()
    return df

def getSymbol(sym):
    conn = sqlite3.connect('stock.db')
    strSQL="SELECT Symbol, Date_Time, Open, High, Low, Close, Volume, Dividends, Stock_Splits, Return, Acc_Return FROM stock WHERE Symbol=:sym"
    df = pd.read_sql_query(strSQL, conn, params={"sym": sym})
    conn.close()
    return df

def calculate_rsi(sym, window=14):
    conn = sqlite3.connect('stock.db')
    strSQL="SELECT Date_Time, Close FROM stock WHERE Symbol=:sym"
    df = pd.read_sql_query(strSQL, conn, params={"sym": sym})
    conn.close()

    df['Date_Time'] = pd.to_datetime(df['Date_Time'])
    df.set_index('Date_Time', inplace=True)

    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    return df

def calculate_volatility(sym, window=21):
    conn = sqlite3.connect('stock.db')
    strSQL="SELECT Date_Time, Close FROM stock WHERE Symbol=:sym"
    df = pd.read_sql_query(strSQL, conn, params={"sym": sym})
    conn.close()

    df['Date_Time'] = pd.to_datetime(df['Date_Time'])
    df.set_index('Date_Time', inplace=True)

    df['Volatility'] = df['Close'].rolling(window=window).std() * np.sqrt(252)
    df['Volatility'] = df['Volatility'] / 100

    return df

def get_stock_data(date_time):
    conn = sqlite3.connect('stock.db')
    strSQL = """
    SELECT Symbol, Open, High, Low, Close, Volume, Dividends, Stock_Splits, Return, Acc_Return 
    FROM stock 
    WHERE Date_Time LIKE :date_time || '%'
    """
    df = pd.read_sql_query(strSQL, conn, params={"date_time": date_time})
    conn.close()

    return df
