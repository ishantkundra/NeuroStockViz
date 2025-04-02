from flask import Flask, render_template, request, jsonify, redirect
import yfinance as yf
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# Dow Jones 30 components
stocks = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "JNJ", "V", "WMT", "JPM", "PG", "UNH",
    "AXP", "BA", "CAT", "CSCO", "CVX", "DIS", "GS", "HD", "HON", "IBM",
    "INTC", "KO", "MCD", "MMM", "MRK", "NKE", "TRV", "WBA", "XOM", "DOW"
]

def get_stock_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date, progress=False, auto_adjust=False)
    if 'Adj Close' in data.columns:
        return data['Adj Close']
    elif 'Close' in data.columns:
        return data['Close']
    else:
        raise KeyError(f"'Adj Close' and 'Close' columns are missing for {ticker}")

def compute_correlations(start_date, end_date):
    df = pd.DataFrame()
    for ticker in stocks:
        try:
            df[ticker] = get_stock_data(ticker, start_date, end_date)
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
    df.dropna(inplace=True)
    return df.corr(method='pearson')

@app.route('/')
def index():
    return redirect('/home')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/visualization')
def visualization():
    return render_template('index.html')


@app.route('/api/correlations', methods=['GET'])
def correlations():
    start_year = request.args.get('start_year', '2014')
    end_year = request.args.get('end_year', '2024')
    selected_stock = request.args.get('selected_stock', None)
    threshold = float(request.args.get('threshold', 0.5))
    start_date = f"{start_year}-01-01"
    end_date = f"{end_year}-12-31"
    
    corr = compute_correlations(start_date, end_date)

    nodes = [{"id": ticker, "group": 1} for ticker in corr.columns]
    edges = []
    for i, ticker1 in enumerate(corr.columns):
        for j, ticker2 in enumerate(corr.columns):
            if i < j:
                corr_value = corr.loc[ticker1, ticker2]
                if abs(corr_value) >= threshold:
                    edge = {
                        "source": ticker1,
                        "target": ticker2,
                        "value": corr_value,
                        "highlight": (selected_stock and (ticker1 == selected_stock or ticker2 == selected_stock))
                    }
                    edges.append(edge)
    
    edges.sort(key=lambda e: abs(e["value"]), reverse=True)

    connected_stocks = set()
    for edge in edges:
        connected_stocks.add(edge["source"])
        connected_stocks.add(edge["target"])

    for ticker in corr.columns:
        if ticker not in connected_stocks:
            nodes.append({"id": ticker, "group": 0})

    correlated_list = []
    non_correlated_list = []
    indirectly_correlated_set = set()
    
    if selected_stock:
        for ticker in corr.columns:
            if ticker == selected_stock:
                continue
            try:
                value = corr.loc[selected_stock, ticker]
                entry = f"{ticker}: {value:.2f}"
                if abs(value) >= threshold:
                    correlated_list.append(entry)
                else:
                    non_correlated_list.append(entry)
            except KeyError:
                continue

    if selected_stock:
        directly_connected = set([e["target"] if e["source"] == selected_stock else e["source"] for e in edges if e["source"] == selected_stock or e["target"] == selected_stock])
        visited = set([selected_stock]) | directly_connected
        queue = list(directly_connected)

        while queue:
            current = queue.pop(0)
            for e in edges:
                if e["source"] == current and e["target"] not in visited:
                    indirectly_correlated_set.add(e["target"])
                    visited.add(e["target"])
                    queue.append(e["target"])
                elif e["target"] == current and e["source"] not in visited:
                    indirectly_correlated_set.add(e["source"])
                    visited.add(e["source"])
                    queue.append(e["source"])

    indirect_list = []
    for ticker in indirectly_correlated_set:
        try:
            value = corr.loc[selected_stock, ticker]
        except KeyError:
            value = 0.0
        indirect_list.append(f"{ticker}: {value:.2f}")
    non_correlated_list = [entry for entry in non_correlated_list if entry.split(":")[0] not in indirectly_correlated_set]

    return jsonify({
        "nodes": nodes,
        "edges": edges,
        "correlated": correlated_list,
        "non_correlated": non_correlated_list,
        "indirectly_correlated": indirect_list
    })

if __name__ == '__main__':
    app.run(debug=True)