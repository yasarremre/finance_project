import pandas as pd
import yfinance as yf
import itertools


def download_data(ticker: str, start: str, end: str) -> pd.DataFrame:
    data = yf.download(ticker, start=start, end=end)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    data = data[['Close']].dropna()
    return data


def moving_average_cross(data: pd.DataFrame, short_window: int, long_window: int) -> float:
    if short_window >= long_window:
        raise ValueError("short_window must be < long_window")

    df = data.copy()
    df['short_ma'] = df['Close'].rolling(window=short_window).mean()
    df['long_ma'] = df['Close'].rolling(window=long_window).mean()

    df['position'] = (df['short_ma'] > df['long_ma']).astype(int)
    df['strategy_return'] = df['position'].shift(1) * df['Close'].pct_change()
    df['strategy_return'] = df['strategy_return'].fillna(0)
    cumulative_return = (1 + df['strategy_return']).prod() - 1
    return cumulative_return


def grid_search(data: pd.DataFrame, short_range: range, long_range: range):
    results = []
    for short, long in itertools.product(short_range, long_range):
        if short >= long:
            continue
        try:
            ret = moving_average_cross(data, short, long)
            results.append({'short_window': short, 'long_window': long, 'return': ret})
        except Exception as e:
            print(f"Skipping short={short}, long={long} due to error: {e}")
    return sorted(results, key=lambda x: x['return'], reverse=True)


if __name__ == "__main__":
    ticker = "THYAO.IS"
    data = download_data(ticker, start="2018-01-01", end="2023-01-01")
    short_range = range(5, 20, 5)
    long_range = range(30, 100, 10)
    results = grid_search(data, short_range, long_range)
    for res in results[:5]:
        print(res)

