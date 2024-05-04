import sys
import streamlit as st
from service.openai_service import generate_financial_summary
from service.fmp_service import get_financial_statements
from utils import sanitize_fmp_response, set_app_env

def financial_statements():
    st.title('GPT-4 & Financial Statements')

    statement_type = st.selectbox("Select financial statement type:", ["Income Statement", "Balance Sheet", "Cash Flow"])

    col1, col2 = st.columns(2)
    with col1:
        period = st.selectbox("Select period:", ["Annual", "Quarterly"]).lower()

    with col2:
        limit = st.number_input("Number of past financial statements to analyze:", min_value=1, max_value=10, value=4)

    ticker = st.text_input("Please enter the company ticker:")

    if st.button('Run'):
        if ticker:
            ticker = ticker.upper()
            financial_statements = get_financial_statements(ticker, limit, period, statement_type)
            if financial_statements is None: st.error("Unable to fetch financial statements. Please ensure the ticker is correct and try again.")

            with st.expander("View Financial Statements"):
                st.dataframe(financial_statements)

            formatted_financial_statements = sanitize_fmp_response(financial_statements, statement_type)
            financial_summary = generate_financial_summary(formatted_financial_statements, statement_type, ticker)
            st.write(f'Summary for {ticker}:\n {financial_summary}\n')

def main(args):
    set_app_env(args[-1])

    st.sidebar.title('AI Financial Analyst')
    app_mode = st.sidebar.selectbox("Choose your AI assistant:", ["Financial Statements"])
    if app_mode == 'Financial Statements':
        financial_statements()

if __name__ == '__main__':
    main(sys.argv[1:])