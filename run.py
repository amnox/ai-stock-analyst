import streamlit as st
from service import get_financial_statements, generate_financial_summary

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
            with st.expander("View Financial Statements"):
                st.dataframe(financial_statements)

            financial_summary = generate_financial_summary(financial_statements, statement_type)
            st.write(f'Summary for {ticker}:\n {financial_summary}\n')

def main():
    st.sidebar.title('AI Financial Analyst')
    app_mode = st.sidebar.selectbox("Choose your AI assistant:",
        ["Financial Statements"])
    if app_mode == 'Financial Statements':
        financial_statements()


if __name__ == '__main__':
    main()