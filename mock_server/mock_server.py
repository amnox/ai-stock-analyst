from flask import Flask, jsonify, request, abort
from mock_data import income_statements_annual, balance_sheets_annual, cash_flow_statements_annual

app = Flask(__name__)


@app.route('/api/v3/<statement_type>/<company>', methods=['GET'])
def get_income_statements(statement_type, company):
    limit = int(request.args.get('limit'))
    period = request.args.get('peroid')
    
    if period is None: period = "annual"
    if limit > 5 or company is None: abort(404)
    
    data = None
    if statement_type == "income-statement":
        if period == "annual":
            data = income_statements_annual[company][:limit]
        else:
            abort(404)
    elif statement_type == "balance-sheet-statement":
        if period == "annual":
            data = balance_sheets_annual[company][:limit]
        else:
            abort(404)
    elif statement_type == "cash-flow-statement":
        if period == "annual":
            data = cash_flow_statements_annual[company][:limit]
        else:
            abort(404)
	
    if data is None: abort(404)
    
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True, port=5000)