import streamlit as st
import openai
import requests
import pandas as pd
from apikey import OPENAI_API_KEY, FMP_API_KEY
openai.api_key = OPENAI_API_KEY

def get_financial_statements(ticker, limit, period, statement_type):
    if statement_type == "Income Statement":
        url = f"https://financialmodelingprep.com/api/v3/income-statement/{ticker}?period={period}&limit={limit}&apikey={FMP_API_KEY}"
    elif statement_type == "Balance Sheet":
        url = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{ticker}?period={period}&limit={limit}&apikey={FMP_API_KEY}"
    elif statement_type == "Cash Flow":
        url = f"https://financialmodelingprep.com/api/v3/cash-flow-statement/{ticker}?period={period}&limit={limit}&apikey={FMP_API_KEY}"
    
    data = get_jsonparsed_data(url)

    if isinstance(data, list) and data:
        return pd.DataFrame(data)
    else:
        st.error("Unable to fetch financial statements. Please ensure the ticker is correct and try again.")
        return pd.DataFrame()
    
def get_jsonparsed_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None

def get_row_data(row):
    output = ""
    for col, val in row.items():
        output += f"{col}: {val}, "
    return output

def generate_financial_summary(financial_statements, statement_type):
    """
    Generate a summary of financial statements for the statements using GPT-3.5 Turbo or GPT-4.
    """
    
    # Create a summary of key financial metrics for all four periods
    summaries = []
    for i in range(len(financial_statements)):
        if statement_type == "Income Statement":
            summary = f"""
                For the period ending {financial_statements['date'][i]}, the company reported the following:
                {get_row_data(financial_statements.iloc[i])}
                """
        elif statement_type == "Balance Sheet":
            summary = f"""
                For the period ending {financial_statements['date'][i]}, the company reported the following:
                {get_row_data(financial_statements.iloc[i])}
                """
        elif statement_type == "Cash Flow":
            summary = f"""
                For the period ending {financial_statements['date'][i]}, the company reported the following:
                {get_row_data(financial_statements.iloc[i])}
                """
        summaries.append(summary)
    # Combine all summaries into a single string
    all_summaries = "\n\n".join(summaries)

    # Call GPT-4 for analysis
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an AI trained to provide financial analysis based on financial statements.",
            },
            {
                "role": "user",
                "content": f"""
                Please analyze the following data and provide insights:\n{all_summaries}.\n 
                Write each section out as instructed in the summary section and then provide analysis of how it's changed over the time period.
                ...
                """
            }
        ]
    )

    return response.choices[0].message.content
