import requests
import yfinance as yf

from datetime import datetime


def fetch_gpw_data_list(tickers :list):
    quotes = yf.download(tickers)
    return quotes

