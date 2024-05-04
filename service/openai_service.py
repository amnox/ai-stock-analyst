import openai
import os
from secrets_keys import OPENAI_API_KEY
openai.api_key = OPENAI_API_KEY

def call_openai_api(all_summaries):
    AI_STOCK_ENV = os.getenv('AI_STOCK_ENV')
    result = ""
    if AI_STOCK_ENV == 'prod' and os.getenv('DISABLE_OPENAI')==False:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI trained to provide financial analysis based on financial statements.",
                },
                {
                    "role": "user",
                    "content": f"""Please analyze the following data and provide insights:\n{all_summaries}.\n Write each section out as instructed in the summary section and then provide analysis of how it's changed over the time period."""
                }
            ]
        )
        result = response.choices[0].message.content
    else:
        result = f"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. \n\n{all_summaries}\n"

    return result

def generate_financial_summary(financial_statements, statement_type, ticker):
    """
    Generate a summary of financial statements for the statements using GPT-3.5 Turbo or GPT-4.
    """
    
    # Create a summary of key financial metrics for all four periods
    summaries = []
    for i in range(len(financial_statements)):
        if statement_type == "Income Statement":
            summary = f"""For the period ending {financial_statements['date'][i]}, the company {ticker} reported the following Income Statements:\n\n{financial_statements.iloc[i].to_csv()}\n"""
        elif statement_type == "Balance Sheet":
            summary = f"""For the period ending {financial_statements['date'][i]}, the company {ticker} reported the following Balance Sheets:\n\n{financial_statements.iloc[i].to_csv()}\n"""
        elif statement_type == "Cash Flow":
            summary = f"""For the period ending {financial_statements['date'][i]}, the company {ticker} reported the following Cash Flow statements:\n\n{financial_statements.iloc[i].to_csv()}\n"""
        summaries.append(summary)
    # Combine all summaries into a single string
    all_summaries = "\n\n".join(summaries)
    return call_openai_api(all_summaries)
