from pymongo import MongoClient
from mock_data import income_statements_annual, balance_sheets_annual, cash_flow_statements_annual

client = MongoClient()
client = MongoClient("localhost", 27017)

db = client['financial_statements_analyst_dev']

income_statements_annual_collection = db["income_statements_annual"]
balance_sheets_annual_collection = db["balance_sheets_annual"]
cash_flow_statements_annual_collection = db["cash_flow_statements_annual"]

# Check if the collection is not empty
if income_statements_annual_collection.count_documents({}) != 0 or balance_sheets_annual_collection.count_documents({}) != 0 or cash_flow_statements_annual_collection.count_documents({}) != 0:
    raise Exception("Collection is not empty. Script execution halted.")

income_statements_annual_collection.insert_many(income_statements_annual["AAPL"])
balance_sheets_annual_collection.insert_many(balance_sheets_annual["AAPL"])
cash_flow_statements_annual_collection.insert_many(cash_flow_statements_annual["AAPL"])

income_statements_annual_collection.insert_many(income_statements_annual["TSLA"])
balance_sheets_annual_collection.insert_many(balance_sheets_annual["TSLA"])
cash_flow_statements_annual_collection.insert_many(cash_flow_statements_annual["TSLA"])
