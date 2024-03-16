# AI Stock Analyst

This app provides financial analysis of publicly traded companies using historical data made available through [SEC](https://www.sec.gov/edgar)

## Pre-requisites
- Open AI API key
- [FMP](https://site.financialmodelingprep.com/pricing-plans) API key

## Setup

Create and activate a python virtual env

```
python3 -m venv openai-env
source ./openai-env/bin/activate
```
Install dependencies

```
python3 -m pip install streamlit openai requests
```
Start the app

```
streamlit run app.py
```
Note: This was made using Python 3.9.6

## Useage

Once the app starts select the desired options and enter the company's ticker in the text box and press run. That will fetch the data and generate the summary for it.

<img width="1728" alt="image" src="https://github.com/amnox/ai-stock-analyst/assets/14812246/76651d6c-2f1c-4b5b-8622-371676ea3134">
