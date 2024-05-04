import requests
from datetime import datetime
import pandas as pd
import os
from secrets_keys import FMP_API_KEY
from utils import get_mongo_collections

# TODO: Test logic for cache miss, and implement cache_data

def get_api_response(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None

def get_cached_data(ticker, limit, period, statement_type):
    income_statements_annual_collection, balance_sheets_annual_collection, cash_flow_statements_annual_collection = get_mongo_collections()
    if period == "annual":
        current_year = int(datetime.now().year)
        required_years = [str(current_year - i) for i in range(1, limit+1)]
        result = []
        if statement_type == "Income Statement":
            result = income_statements_annual_collection.find({"calendarYear": {"$in": required_years}, "symbol": ticker}, {"_id": 0})
        elif statement_type == "Balance Sheet":
            result = balance_sheets_annual_collection.find({"calendarYear": {"$in": required_years}, "symbol": ticker}, {"_id": 0})
        elif statement_type == "Cash Flow":
            result = cash_flow_statements_annual_collection.find({"calendarYear": {"$in": required_years}, "symbol": ticker}, {"_id": 0})

        results_list = [i for i in result]

        if len(results_list)<len(required_years):
            return None
        else:
            return results_list
    return None

def cache_data(data, ticker, limit, period, statement_type):
    income_statements_annual_collection, balance_sheets_annual_collection, cash_flow_statements_annual_collection = get_mongo_collections()

    current_collection = None
    if statement_type == "Income Statement":
        current_collection = income_statements_annual_collection
    elif statement_type == "Balance Sheet":
        current_collection = balance_sheets_annual_collection
    elif statement_type == "Cash Flow":
        current_collection = cash_flow_statements_annual_collection
    dates_in_response = [date['calendarYear'] for date in data]

    for index, date in enumerate(dates_in_response):
        if not current_collection.find_one({"calendarYear" : date, "symbol": ticker}):
            current_collection.insert_one(data[index])

def get_dataframe(data):
    if isinstance(data, list) and data:
        return pd.DataFrame(data)
    else:
        return None
def get_financial_statements(ticker, limit, period, statement_type):
    FMP_URL = os.getenv('FMP_URL')

    cached_data = get_dataframe(get_cached_data(ticker, limit, period, statement_type))
    
    if cached_data is not None:
        return cached_data

    if statement_type == "Income Statement":
        url = f"{FMP_URL}api/v3/income-statement/{ticker}?period={period}&limit={limit}&apikey={FMP_API_KEY}"
    elif statement_type == "Balance Sheet":
        url = f"{FMP_URL}api/v3/balance-sheet-statement/{ticker}?period={period}&limit={limit}&apikey={FMP_API_KEY}"
    elif statement_type == "Cash Flow":
        url = f"{FMP_URL}api/v3/cash-flow-statement/{ticker}?period={period}&limit={limit}&apikey={FMP_API_KEY}"
    
    data = get_api_response(url)
    
    cache_data(data, ticker, limit, period, statement_type)

    return get_dataframe(data)