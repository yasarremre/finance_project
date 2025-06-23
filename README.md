# Finance Project

This repository contains scripts for experimenting with trading strategies on Turkish stocks. The `param_test.py` script downloads historical data for THYAO (Turkish Airlines) from Yahoo Finance and performs a simple grid search over moving average parameters.

## Usage

1. Install the required Python packages:
   ```bash
   pip install pandas yfinance
   ```

2. Run the script:
   ```bash
   python param_test.py
   ```
   The script prints the top parameter combinations ranked by cumulative return.

The example uses daily data between 2018 and 2023 and tests different short and long moving average windows. You can modify the ticker, date range, or parameter ranges directly in `param_test.py`.


### Docker

You can also run the script in a Docker container:

```bash
docker build -t finance-test .
docker run --rm finance-test
```

This builds an image using `Dockerfile` and executes `param_test.py` inside a container.
