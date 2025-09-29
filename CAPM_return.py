import datetime
import streamlit as st
import pandas as pd
import yfinance as yf
import CAPM_function
import plotly.graph_objects as go

# Ensure Date column presence and flatten columns and index properly
def prepare_yfinance_data(ticker, start, end, rename_to):
    df = yf.download(ticker, start=start, end=end)
    
    if df.empty:
        raise ValueError(f"No data downloaded for ticker {ticker}")

    df.reset_index(inplace=True)

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ['_'.join(filter(None, map(str, col))).strip() for col in df.columns.values]

    date_column = None
    possible_date_names = ['Date', 'date', 'Datetime', 'datetime', 'index']
    
    for col in df.columns:
        if col in possible_date_names or 'date' in col.lower():
            date_column = col
            break
    
    if date_column is None:
        if pd.api.types.is_datetime64_any_dtype(df.iloc[:, 0]):
            date_column = df.columns[0]
    
    if date_column is None:
        raise KeyError(f"Date column not found for ticker {ticker}. Available columns: {df.columns.tolist()}")
    
    if date_column != 'Date':
        df.rename(columns={date_column: 'Date'}, inplace=True)

    close_cols = [col for col in df.columns if 'Close' in col or 'close' in col.lower()]
    if not close_cols:
        close_cols = [col for col in df.columns if 'adj' in col.lower() and ('close' in col.lower() or 'price' in col.lower())]
    
    if not close_cols:
        raise KeyError(f"Close price column not found for ticker {ticker}. Available columns: {df.columns.tolist()}")
    
    close_col = close_cols[0]

    df = df[['Date', close_col]].copy()
    df.rename(columns={close_col: rename_to}, inplace=True)
    df['Date'] = pd.to_datetime(df['Date'])
    
    return df

def get_risk_interpretation(beta):
    if beta < 0:
        return "Negative Beta (Inverse Market Relationship)", "🔵"
    elif beta < 0.8:
        return "Low Volatility (Defensive)", "🟢"
    elif beta < 1.2:
        return "Market Average", "🟡"
    elif beta < 1.5:
        return "High Volatility (Aggressive)", "🟠"
    else:
        return "Very High Volatility (Very Aggressive)", "🔴"

def get_recommendations(beta, expected_return, stock):
    risk_cat, _ = get_risk_interpretation(beta)
    
    recommendations = []
    
    if beta < 0:
        recommendations.append(f"✓ {stock} moves inversely to the market - good for hedging")
        recommendations.append(f"✓ Consider for portfolio diversification during market downturns")
    elif beta < 0.8:
        recommendations.append(f"✓ {stock} is less volatile than the market - suitable for conservative investors")
        recommendations.append(f"✓ Good for capital preservation and steady returns")
    elif beta < 1.2:
        recommendations.append(f"✓ {stock} moves in line with the market - balanced risk/reward")
        recommendations.append(f"✓ Suitable for moderate risk tolerance investors")
    elif beta < 1.5:
        recommendations.append(f"⚠ {stock} is more volatile than the market - higher risk and potential reward")
        recommendations.append(f"⚠ Suitable for growth-oriented investors with higher risk tolerance")
    else:
        recommendations.append(f"⚠ {stock} is highly volatile - significant risk and potential reward")
        recommendations.append(f"⚠ Only suitable for aggressive investors comfortable with large price swings")
    
    if expected_return > 20:
        recommendations.append(f"📈 High expected annual return of {expected_return:.2f}%")
    elif expected_return > 10:
        recommendations.append(f"📊 Moderate expected annual return of {expected_return:.2f}%")
    else:
        recommendations.append(f"📉 Conservative expected annual return of {expected_return:.2f}%")
    
    return recommendations

# Page config
st.set_page_config(page_title="CAPM Return Calculator", page_icon="📈", layout="wide")

# Header with explanation
st.title("📊 Capital Asset Pricing Model (CAPM) Analysis")
st.markdown("""
---
### 📚 What is CAPM?
The **Capital Asset Pricing Model (CAPM)** helps investors understand the relationship between risk and expected return. 
It calculates the expected return of an investment based on its systematic risk (Beta) relative to the market.

**Formula:** `Expected Return = Risk-Free Rate + Beta × (Market Return - Risk-Free Rate)`
""")

with st.expander("ℹ️ Understanding Key Metrics"):
    st.markdown("""
    - **Beta (β)**: Measures a stock's volatility relative to the market
        - β = 1: Stock moves with the market
        - β > 1: Stock is more volatile than the market
        - β < 1: Stock is less volatile than the market
        - β < 0: Stock moves inversely to the market
    
    - **Alpha (α)**: The y-intercept of the regression line, representing stock-specific returns
    
    - **Expected Return**: The annual return predicted by CAPM based on the stock's risk profile
    
    - **Risk-Free Rate**: The return of a risk-free investment (U.S. Treasury bonds) - currently set to 0% for simplicity
    """)

st.markdown("---")

# Input section
col1, col2 = st.columns([1, 1])
with col1:
    stocks_list = st.multiselect(
        "📈 Select your stocks:",
        ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'JPM', 'V',
         'UNH', 'HD', 'PG', 'MA', 'DIS', 'PYPL', 'BAC', 'VZ', 'ADBE', 'CMCSA', 'NFLX'],
        ['AAPL', 'MSFT', 'GOOGL']
    )
with col2:
    year = st.number_input("📅 Number of Years for Analysis", min_value=1, max_value=10, value=1)

end = datetime.date.today()
start = datetime.date(end.year - year, end.month, end.day)

if not stocks_list:
    st.info("👆 Please select at least one stock to begin the analysis")
    st.stop()

try:
    with st.spinner('📥 Downloading market data...'):
        sp500_data = prepare_yfinance_data('^GSPC', start, end, 'sp500')

        stock_dfs = []
        failed_stocks = []
        for stock in stocks_list:
            try:
                stock_df = prepare_yfinance_data(stock, start, end, stock)
                stock_dfs.append(stock_df)
            except Exception as e:
                failed_stocks.append(stock)
                st.warning(f"⚠️ Could not download data for {stock}: {str(e)}")

        if failed_stocks:
            stocks_list = [s for s in stocks_list if s not in failed_stocks]

        if not stock_dfs:
            st.error("❌ No valid stock data available. Please select different stocks.")
            st.stop()

        merged_stocks = stock_dfs[0]
        for df in stock_dfs[1:]:
            merged_stocks = pd.merge(merged_stocks, df, on='Date', how='inner')

        merged_df = pd.merge(merged_stocks, sp500_data, on='Date', how='inner')

        if merged_df.empty:
            st.error("❌ No overlapping dates found. Please try a different date range.")
            st.stop()

    st.success(f"✅ Successfully loaded data for {len(stocks_list)} stocks from {start} to {end}")
    
    st.markdown("---")
    st.header("📊 Raw Data Overview")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### 📋 Dataframe Head")
        st.dataframe(merged_df.head(), use_container_width=True)
    with col2:
        st.markdown("### 📋 Dataframe Tail")
        st.dataframe(merged_df.tail(), use_container_width=True)

    valid_stocks = [col for col in merged_df.columns if col != 'Date' and col != 'sp500']

    st.markdown("---")
    st.header("📈 Price Visualization")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### 💵 Absolute Price")
        plot_df = merged_df[['Date'] + valid_stocks].copy()
        st.plotly_chart(CAPM_function.interactive_plot(plot_df), use_container_width=True)
    with col2:
        st.markdown("### 📊 Normalized Price (Base = 1)")
        plot_df = merged_df[['Date'] + valid_stocks].copy()
        st.plotly_chart(CAPM_function.interactive_plot(CAPM_function.normalize(plot_df)), use_container_width=True)

    st.markdown("""
    **💡 Interpretation:**
    - **Absolute Price**: Shows actual stock prices over time
    - **Normalized Price**: Shows relative performance - all stocks start at 1.0 for easy comparison
    """)

    stocks_daily_return = CAPM_function.daily_return(merged_df)

    st.markdown("---")
    st.header("📉 Daily Returns Analysis")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### 📋 Daily Returns Head")
        st.dataframe(stocks_daily_return.head(), use_container_width=True)
    with col2:
        st.markdown("### 📋 Daily Returns Tail")
        st.dataframe(stocks_daily_return.tail(), use_container_width=True)

    st.markdown("""
    **💡 Daily Returns**: Shows the percentage change in price from one day to the next. 
    These values are used to calculate Beta and expected returns.
    """)

    beta = {}
    alpha = {}
    for stock in valid_stocks:
        if stock in stocks_daily_return.columns:
            b, a = CAPM_function.calculate_beta(stocks_daily_return, stock)
            beta[stock] = b
            alpha[stock] = a

    st.markdown("---")
    st.header("🎯 CAPM Results & Analysis")

    col1, col2 = st.columns([1, 1])
    
    beta_df = pd.DataFrame(columns=['Stock', 'Beta Value', 'Risk Category', 'Risk Indicator'])
    beta_df['Stock'] = beta.keys()
    beta_df['Beta Value'] = [round(i, 3) for i in beta.values()]
    risk_info = [get_risk_interpretation(b) for b in beta.values()]
    beta_df['Risk Category'] = [r[0] for r in risk_info]
    beta_df['Risk Indicator'] = [r[1] for r in risk_info]
    
    with col1:
        st.markdown("### 📊 Beta Values & Risk Profile")
        st.dataframe(beta_df, use_container_width=True)
    
    rf = 0  # Risk-free rate
    rm = stocks_daily_return['sp500'].mean() * 252  # Annualized market return
    
    return_df = pd.DataFrame()
    return_value = []
    for stock, value in beta.items():
        expected_return = rf + value * (rm - rf)
        return_value.append(round(expected_return, 2))
    
    return_df['Stock'] = list(beta.keys())
    return_df['Expected Annual Return (%)'] = return_value
    return_df['Beta'] = [round(b, 3) for b in beta.values()]

    with col2:
        st.markdown("### 💰 Expected Returns (CAPM)")
        st.dataframe(return_df, use_container_width=True)

    st.markdown(f"""
    **📊 Market Context:**
    - **S&P 500 Annualized Return**: {rm:.2f}%
    - **Risk-Free Rate**: {rf:.2f}%
    - **Analysis Period**: {year} year(s)
    """)

    # Scatter plot: Beta vs Expected Return
    st.markdown("---")
    st.header("📈 Risk-Return Visualization")
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=return_df['Beta'],
        y=return_df['Expected Annual Return (%)'],
        mode='markers+text',
        marker=dict(size=15, color=return_df['Expected Annual Return (%)'], 
                   colorscale='RdYlGn', showscale=True, 
                   colorbar=dict(title="Expected Return %")),
        text=return_df['Stock'],
        textposition="top center",
        textfont=dict(size=10, color='black'),
        name='Stocks'
    ))
    
    fig.add_trace(go.Scatter(
        x=[1], y=[rm], mode='markers+text',
        marker=dict(size=20, color='blue', symbol='star'),
        text=['Market (S&P 500)'], textposition="top center",
        name='Market Benchmark'
    ))
    
    fig.update_layout(
        title="Risk vs Return Profile",
        xaxis_title="Beta (Systematic Risk)",
        yaxis_title="Expected Annual Return (%)",
        hovermode='closest',
        height=500,
        showlegend=True
    )
    
    fig.add_hline(y=rm, line_dash="dash", line_color="blue", 
                  annotation_text="Market Return")
    fig.add_vline(x=1, line_dash="dash", line_color="gray", 
                  annotation_text="Market Beta")
    
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    **💡 Interpretation:**
    - Stocks **above the market return line** may offer better risk-adjusted returns
    - Stocks with **Beta < 1** (left of vertical line) are less volatile than the market
    - Stocks with **Beta > 1** (right of vertical line) are more volatile than the market
    """)

    # Individual stock analysis
    st.markdown("---")
    st.header("🔍 Individual Stock Analysis & Recommendations")
    
    for stock in stocks_list:
        if stock in beta:
            with st.expander(f"📊 {stock} - Detailed Analysis"):
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.markdown(f"### Key Metrics")
                    stock_beta = beta[stock]
                    stock_return = rf + stock_beta * (rm - rf)
                    risk_cat, risk_emoji = get_risk_interpretation(stock_beta)
                    
                    st.metric("Beta (β)", f"{stock_beta:.3f}")
                    st.metric("Expected Annual Return", f"{stock_return:.2f}%")
                    st.metric("Risk Category", f"{risk_emoji} {risk_cat}")
                    st.metric("Alpha (α)", f"{alpha[stock]:.4f}")
                
                with col2:
                    st.markdown(f"### 💡 Investment Recommendations")
                    recommendations = get_recommendations(stock_beta, stock_return, stock)
                    for rec in recommendations:
                        st.markdown(f"- {rec}")
                
                # Regression plot for individual stock
                x_vals = stocks_daily_return['sp500'].values
                y_vals = stocks_daily_return[stock].values
                
                fig_reg = go.Figure()
                fig_reg.add_trace(go.Scatter(
                    x=x_vals, y=y_vals, mode='markers',
                    marker=dict(size=5, opacity=0.5),
                    name='Daily Returns'
                ))
                
                # Regression line
                x_line = sorted(x_vals)
                y_line = [alpha[stock] + stock_beta * x for x in x_line]
                fig_reg.add_trace(go.Scatter(
                    x=x_line, y=y_line, mode='lines',
                    line=dict(color='red', width=2),
                    name=f'Regression Line (β={stock_beta:.3f})'
                ))
                
                fig_reg.update_layout(
                    title=f"{stock} vs S&P 500 - Beta Calculation",
                    xaxis_title="S&P 500 Daily Return (%)",
                    yaxis_title=f"{stock} Daily Return (%)",
                    height=400
                )
                
                st.plotly_chart(fig_reg, use_container_width=True)

    # Portfolio summary
    st.markdown("---")
    st.header("📁 Portfolio Summary")
    
    col1, col2, col3 = st.columns(3)
    
    avg_beta = sum(beta.values()) / len(beta)
    avg_return = sum(return_value) / len(return_value)
    
    with col1:
        st.metric("📊 Portfolio Avg Beta", f"{avg_beta:.3f}")
    with col2:
        st.metric("💰 Portfolio Avg Return", f"{avg_return:.2f}%")
    with col3:
        st.metric("📈 Number of Stocks", len(stocks_list))
    
    st.markdown("""
    ---
    ### 🎓 Final Investment Insights
    """)
    
    if avg_beta < 1:
        st.info("""
        🟢 **Conservative Portfolio**: Your portfolio has an average Beta less than 1, indicating lower volatility 
        than the market. This is suitable for risk-averse investors seeking stable returns.
        """)
    elif avg_beta > 1.2:
        st.warning("""
        🔴 **Aggressive Portfolio**: Your portfolio has an average Beta greater than 1.2, indicating higher volatility 
        than the market. This offers higher potential returns but comes with increased risk.
        """)
    else:
        st.success("""
        🟡 **Balanced Portfolio**: Your portfolio has an average Beta close to 1, indicating it moves in line with 
        the market. This offers a balanced risk-return profile.
        """)

    st.markdown("""
    ---
    ### ⚠️ Important Disclaimer
    This analysis is for **educational purposes only** and should not be considered as financial advice. 
    Past performance does not guarantee future results. Please consult with a qualified financial advisor 
    before making investment decisions.
    """)

except Exception as e:
    st.error(f"❌ An error occurred: {str(e)}")
    st.exception(e)