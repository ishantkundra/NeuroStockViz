from flask import Flask, render_template, request, jsonify
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
    # Explicitly select the desired column
    if 'Adj Close' in data.columns:
        return data['Adj Close']
    elif 'Close' in data.columns:
        return data['Close']
    else:
        raise KeyError(f"'Adj Close' and 'Close' columns are missing for {ticker}")

def compute_correlations(start_date, end_date):
    # Collect adjusted closing prices for each stock
    df = pd.DataFrame()
    for ticker in stocks:
        try:
            df[ticker] = get_stock_data(ticker, start_date, end_date)
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
    # Remove days with missing data
    df.dropna(inplace=True)
    # Calculate Pearson’s correlation matrix
    corr = df.corr(method='pearson')
    return corr

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/correlations', methods=['GET'])
def correlations():
    # Get query parameters for time range and selected stock
    start_year = request.args.get('start_year', '2014')
    end_year = request.args.get('end_year', '2024')
    selected_stock = request.args.get('selected_stock', None)
    
    # Build date strings for data fetching
    start_date = f"{start_year}-01-01"
    end_date = f"{end_year}-12-31"
    
    corr = compute_correlations(start_date, end_date)
    
    # Prepare nodes (stocks) and edges (significant correlations) for visualization
    nodes = [{"id": ticker, "group": 1} for ticker in corr.columns]
    edges = []
    threshold = 0.5  # threshold to filter weaker correlations
    for i, ticker1 in enumerate(corr.columns):
        for j, ticker2 in enumerate(corr.columns):
            if i < j:
                corr_value = corr.loc[ticker1, ticker2]
                if abs(corr_value) >= threshold:
                    edge = {"source": ticker1, "target": ticker2, "value": corr_value}
                    # Flag edges related to the selected stock for highlighting
                    if selected_stock and (ticker1 == selected_stock or ticker2 == selected_stock):
                        edge["highlight"] = True
                    else:
                        edge["highlight"] = False
                    edges.append(edge)
    
    return jsonify({"nodes": nodes, "edges": edges})

if __name__ == '__main__':
    app.run(debug=True)
