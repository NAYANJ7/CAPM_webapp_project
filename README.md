# 📊 CAPM Stock Analysis Dashboard

A comprehensive web application built with Streamlit that performs Capital Asset Pricing Model (CAPM) analysis on stocks, helping investors understand risk-return relationships and make informed investment decisions.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🌟 Features

- **Interactive Stock Selection**: Choose from 20 popular stocks including AAPL, MSFT, GOOGL, AMZN, TSLA, and more
- **Historical Data Analysis**: Analyze stock performance over 1-10 years
- **CAPM Calculations**: Automatic Beta, Alpha, and expected return calculations
- **Risk Profiling**: Intelligent risk categorization (Defensive, Market Average, Aggressive, etc.)
- **Visual Analytics**: 
  - Price charts (absolute and normalized)
  - Risk vs Return scatter plots
  - Individual stock regression analysis
  - Beta visualization
- **Investment Recommendations**: Personalized recommendations based on risk tolerance
- **Portfolio Summary**: Aggregate portfolio metrics and insights
- **Educational Content**: Built-in explanations of CAPM concepts and metrics

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/NAYANJ7/capm-stock-analysis.git
cd capm-stock-analysis
```

2. Install required packages:
```bash
pip install streamlit pandas numpy yfinance plotly
```

3. Run the application:
```bash
streamlit run CAPM_return.py
```

4. Open your browser and navigate to:
```
http://localhost:8501
```

## 📦 Dependencies

- streamlit >= 1.28.0
- pandas >= 2.0.0
- numpy >= 1.24.0
- yfinance >= 0.2.28
- plotly >= 5.17.0

Install all dependencies at once:
```bash
pip install streamlit pandas numpy yfinance plotly
```

## 📁 Project Structure

```
capm-stock-analysis/
│
├── CAPM_return.py          # Main Streamlit application
├── CAPM_function.py        # Helper functions for calculations
└── README.md              # Project documentation
```

## 🧮 How CAPM Works

The **Capital Asset Pricing Model (CAPM)** calculates the expected return of an investment based on its systematic risk:

```
Expected Return = Risk-Free Rate + Beta × (Market Return - Risk-Free Rate)
```

### Key Metrics Explained

- **Beta (β)**: Measures volatility relative to the market
  - β = 1: Moves with the market
  - β > 1: More volatile than the market
  - β < 1: Less volatile than the market
  - β < 0: Inverse relationship with the market

- **Alpha (α)**: Stock-specific returns independent of market movements

- **Expected Return**: Predicted annual return based on risk profile

## 🎯 Usage Guide

### 1. Select Stocks
Choose one or more stocks from the dropdown menu. The default selection includes major tech stocks (AAPL, MSFT, GOOGL, AMZN, TSLA, META).

### 2. Choose Time Period
Select the analysis period from 1 to 10 years using the number input.

### 3. Analyze Results
Review the comprehensive analysis including:
- Historical price data
- Daily returns
- Beta calculations
- Expected returns
- Risk categorization
- Investment recommendations

### 4. Individual Stock Deep Dive
Expand individual stock sections to see:
- Detailed metrics
- Regression analysis
- Specific recommendations

### 5. Portfolio Overview
Check the portfolio summary for aggregate metrics and overall investment strategy guidance.

## 📊 Understanding the Visualizations

### Price Charts
- **Absolute Price**: Raw stock prices over time
- **Normalized Price**: All stocks start at 1.0 for easy comparison

### Risk-Return Plot
- X-axis: Beta (systematic risk)
- Y-axis: Expected annual return
- Blue star: Market benchmark (S&P 500)
- Dashed lines: Market Beta (x=1) and Market Return (horizontal)

### Regression Plots
- Show the relationship between stock returns and market returns
- Slope of the line = Beta
- Scatter points = Daily return observations

## 🔧 Customization

### Adding More Stocks

Edit the stock list in `CAPM_return.py`:

```python
stocks_list = st.multiselect(
    "📈 Select your stocks:",
    ['AAPL', 'MSFT', 'YOUR_STOCK_HERE'],  # Add your ticker
    ['AAPL', 'MSFT']
)
```

### Adjusting Risk-Free Rate

Modify the `rf` variable in `CAPM_return.py`:

```python
rf = 0.04  # 4% risk-free rate (e.g., 10-year Treasury yield)
```

### Changing Chart Dimensions

Edit the `interactive_plot` function in `CAPM_function.py`:

```python
fig.update_layout(
    width=600,  # Change width
    height=400,  # Change height
    ...
)
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 To-Do / Future Enhancements

- [ ] Add export functionality (PDF/Excel reports)
- [ ] Include Sharpe Ratio calculations
- [ ] Add portfolio optimization features
- [ ] Implement Monte Carlo simulations
- [ ] Add comparison with industry benchmarks
- [ ] Include fundamental analysis metrics
- [ ] Add real-time data updates
- [ ] Implement user authentication for saved portfolios
- [ ] Add cryptocurrency support
- [ ] Include international stock markets

## ⚠️ Disclaimer

This application is for **educational and informational purposes only**. It should not be considered as financial advice. 

- Past performance does not guarantee future results
- Stock market investments carry risk of loss
- CAPM has limitations and assumptions that may not hold in real markets
- Always consult with a qualified financial advisor before making investment decisions
- The developers are not responsible for any financial losses incurred from using this tool

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Nayan Jain**
- GitHub: [@NAYANJ7](https://github.com/NAYANJ7)
- LinkedIn: [Nayan Jain](https://www.linkedin.com/in/nayan-jain007/)

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing web framework
- [yfinance](https://github.com/ranaroussi/yfinance) for stock data API
- [Plotly](https://plotly.com/) for interactive visualizations
- The open-source community for inspiration and support

## 📚 References

- Sharpe, W. F. (1964). "Capital asset prices: A theory of market equilibrium under conditions of risk"
- Modern Portfolio Theory by Harry Markowitz
- [Investopedia - CAPM](https://www.investopedia.com/terms/c/capm.asp)

## 📞 Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Contact the maintainer

---

⭐ If you find this project useful, please consider giving it a star on GitHub!

**Made with ❤️ and Python**
