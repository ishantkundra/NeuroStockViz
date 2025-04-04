🧠 NeuroStockViz

Visualizing Stock Correlations as Neural Networks
CSCE 679: Data Visualization — Spring 2025
Instructor: Prof. Meng Xia
Developed by:
	•	Ishant Kundra
	•	Rahaan Gandhi
	•	Tanishq Chopra

⸻

📌 Project Overview

NeuroStockViz is a multi-view, interactive data visualization platform that enables exploration of Dow Jones 30 stock relationships through various analytics views including neural network layouts, heatmaps, clusters, and candlestick charts.

Built as a final project for Texas A&M University’s Spring 2025 CSCE 679: Data Visualization course.

⸻

🧠 Features

View	Description
Neural Network Graph	Explore stock correlations as an interactive network graph.
Time-Series Mini Chart	Compare two stocks’ historical trends with a line chart.
Correlation Heatmap	Visualize pairwise Pearson correlation between all 30 stocks.
Cluster View	K-Means clustering based on correlation patterns.
Candlestick Chart	Interactive OHLC view of a selected stock over a selected time range.



⸻

🧱 Tech Stack
	•	Frontend: HTML5, CSS3, JavaScript, Chart.js, D3.js, Lightweight-Charts
	•	Backend: Python, Flask, yFinance, Pandas, Scikit-Learn
	•	Data Source: Yahoo Finance via yfinance API

⸻

📁 Project Structure

NeuroStockViz/
├── static/
│   └── images/                   # Icons & visual previews
│       ├── candlestick.jpg
│       ├── cluster.png
│       ├── head.jpg
│       ├── heatmap.jpg
│       ├── line.jpg
│       └── ncn.jpg
├── templates/                    # HTML files for each visualization view
│   ├── candlestick.html
│   ├── clusters.html
│   ├── heatmap.html
│   ├── home.html
│   ├── index.html               # Neural correlation network view
│   └── minichart.html
├── app.py                        # Flask application routing and backend logic
├── LICENSE
├── README.md                     # Project documentation
└── .gitignore



⸻

🚀 Getting Started

1. Clone the Repository

git clone https://github.com/ishantkundra/NeuroStockViz.git
cd NeuroStockViz

2. Install Python Dependencies

pip install flask yfinance pandas scikit-learn flask-caching

Optionally, create a requirements.txt using:

pip freeze > requirements.txt



3. Run the Application

python app.py

4. Open in Browser

Visit: http://localhost:5000

⸻

🖼️ Preview Screenshots

Home Page	Neural Correlation Network
	

Time-Series Chart	Heatmap View
	

Stock Clustering View	Candlestick Chart
	



⸻

📌 Use Cases
	•	Compare sector-based performance.
	•	Identify strongly correlated or anti-correlated stocks.
	•	Track individual stock price trends via technical analysis.
	•	Uncover hidden structure via clustering techniques.

⸻

🔮 Future Enhancements
	•	Add hover tooltips for technical details in candlestick view.
	•	Export charts as PNG/PDF.
	•	Add historical performance comparison table.
	•	Extend to NASDAQ-100 or S&P 500 support.

⸻

📝 License

MIT License — for educational and academic purposes.
