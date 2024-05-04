import json, os
from pymongo import MongoClient


def sanitize_fmp_response(financial_statements, statement_type):
    columns_to_drop = []

    if statement_type == "Income Statement":
        columns_to_drop = ['acceptedDate', 'fillingDate', 'period', 'reportedCurrency', 'symbol', 'finalLink', 'link', 'period']
    elif statement_type == "Balance Sheet":
        columns_to_drop = ['acceptedDate', 'fillingDate', 'period', 'reportedCurrency', 'symbol', 'finalLink', 'link', 'period']
    elif statement_type == "Cash Flow":
        columns_to_drop = ['acceptedDate', 'fillingDate', 'period', 'reportedCurrency', 'symbol', 'finalLink', 'link', 'period']
    
    return financial_statements.drop(columns=columns_to_drop, axis=1)


def set_app_env(current_env):
    with open('config/dev.json', 'r') as file:
        dev_vars = json.load(file)

    with open('config/prod.json', 'r') as file:
        prod_vars = json.load(file)

    if current_env == "prod":
        os.environ['AI_STOCK_ENV'] = 'prod'
        os.environ['FMP_URL'] = prod_vars['fmp-api']
        os.environ['MONGO_URL'] = prod_vars['mongodb']['url']
        os.environ['MONGO_PORT'] = prod_vars['mongodb']['port']
        os.environ['DB_NAME'] = prod_vars['mongodb']['db']
        os.environ['DISABLE_OPENAI'] = prod_vars['disable_openai']
    else:
        os.environ['AI_STOCK_ENV'] = 'dev'
        os.environ['FMP_URL'] = dev_vars['fmp-api']
        os.environ['MONGO_URL'] = dev_vars['mongodb']['url']
        os.environ['MONGO_PORT'] = dev_vars['mongodb']['port']
        os.environ['DB_NAME'] = dev_vars['mongodb']['db']
        os.environ['DISABLE_OPENAI'] = prod_vars['disable_openai']

def get_mongo_collections():
    client = MongoClient()
    client = MongoClient(os.getenv('MONGO_URL'), int(os.getenv('MONGO_PORT')))

    db = client[os.getenv('DB_NAME')]

    income_statements_annual_collection = db["income_statements_annual"]
    balance_sheets_annual_collection = db["balance_sheets_annual"]
    cash_flow_statements_annual_collection = db["cash_flow_statements_annual"]

    return income_statements_annual_collection, balance_sheets_annual_collection, cash_flow_statements_annual_collection