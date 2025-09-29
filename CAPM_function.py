import numpy as np
import plotly.express as px

def interactive_plot(df):
    fig = px.line()
    for col in df.columns:
        if col != 'Date':
            fig.add_scatter(x=df['Date'], y=df[col], mode='lines', name=col)
    fig.update_layout(
        width=450,
        margin=dict(l=20, r=20, t=20, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig

def normalize(df_2):
    df = df_2.copy()
    for col in df.columns:
        if col != 'Date':
            df[col] = df[col] / df[col].iloc[0]
    return df

def daily_return(df):
    df_daily_return = df.copy()
    for col in df.columns:
        if col != 'Date':
            df_daily_return[col] = df[col].pct_change().fillna(0) * 100
    return df_daily_return

def calculate_beta(stock_daily_return, stock):
    x = stock_daily_return['sp500'].values
    y = stock_daily_return[stock].values
    b, a = np.polyfit(x, y, 1)
    return b, a
