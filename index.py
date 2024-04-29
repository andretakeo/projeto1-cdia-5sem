from flask import Flask
from flask import request,Response
import os
import sqlite3
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
import numpy as np
import sqlite3

from utils import *




app = Flask(__name__)
#orient={‘split’, ‘records’, ‘index’, ‘table’}.
@app.route("/",methods=['GET'])
def index():
    df=getAll()
    return Response(df.to_json(orient="records"), mimetype='application/json')


@app.route("/all-symbols",methods=['GET'])
def getSYMS():
    df=showSymbols()
    return Response(df.to_json(), mimetype='application/json')


@app.route("/symbol/<sym>", methods=['GET'])
def getSYM(sym):
    df = getSymbol(sym.to_upper())
    return Response(df.to_json(orient="records"), mimetype='application/json')


@app.route("/rsi/<sym>", methods=['GET'])
def getRSI(sym):
    df = calculate_rsi(sym.to_upper())
    fig = Figure(figsize=(12, 8))
    axis = fig.add_subplot(1, 1, 1)
    axis.plot(df.index, df['RSI'], label='RSI', color='orange')  
    axis.axhline(y=70, color='r', linestyle='--', label='Overbought (70)')  # Overbought line
    axis.axhline(y=30, color='g', linestyle='--', label='Oversold (30)')  # Oversold line
    axis.set_title('Indicador RSI')
    axis.set_xlabel('')
    axis.set_ylabel('')
    axis.legend()
    fig.autofmt_xdate()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route("/volatility/<sym>", methods=['GET'])
def getVolatility(sym):
    df = calculate_volatility(sym.to_upper())
    fig = Figure(figsize=(12, 8))
    axis = fig.add_subplot(1, 1, 1)
    axis.plot(df.index, df['Volatility'], label='Janela de 21 dias', color='blue')  
    axis.set_title('Volatilidade%')
    axis.set_xlabel('')
    axis.set_ylabel('')
    axis.legend()
    fig.autofmt_xdate()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route("/stock-data/<date_time>", methods=['GET'])
def getStockData(date_time):
    df = get_stock_data(date_time)
    return Response(df.to_json(orient="records"), mimetype='application/json')


if __name__=="__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'), 
            port=int(os.getenv('PORT', 5000)))
