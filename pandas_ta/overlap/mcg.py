# -*- coding: utf-8 -*-
from pandas_ta.utils import get_offset, verify_series


def mcg(close, length: int = 10, offset: int = 0, c: float = 1, **kwargs):
    """Indicator: McGinley Dynamic Indicator"""
    # Validate arguments
    close = verify_series(close)
    length = int(length) if length > 0 else 10
    c = c if 1 >= c > 0 else 1
    offset = get_offset(offset)

    # Calculate Result
    close = close.copy()

    def mcg_(series):
        denom = (c * length * (series.iloc[1] / series.iloc[0]) ** 4)
        series.iloc[1] = (series.iloc[0] + ((series.iloc[1] - series.iloc[0]) / denom))
        return series.iloc[1]

    mcg_cell = close[0:].rolling(2, min_periods=2).apply(mcg_, raw=False)
    mcg_ds = close[:1].append(mcg_cell[1:])

    # Offset
    if offset != 0:
        mcg_ds = mcg_ds.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        mcg_ds.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        mcg_ds.fillna(method=kwargs["fill_method"], inplace=True)

    # Name & Category
    mcg_ds.name = f"McGinley_{length}"
    mcg_ds.category = 'overlap'

    return mcg_ds


mcg.__doc__ = \
"""McGinley Dynamic Indicator

The McGinley Dynamic looks like a moving average line, yet it is actually a smoothing mechanism
for prices that minimizes price separation, price whipsaws, and hugs prices much more closely. 
Because of the calculation, the Dynamic Line speeds up in down markets as it follows prices 
yet moves more slowly in up markets.

Sources:
    https://www.investopedia.com/articles/forex/09/mcginley-dynamic-indicator.asp

Calculation:
    Default Inputs:
        length=10
        offset=0
        c=1
        
    def mcg_(series):
        denom = (constant * length * (series.iloc[1] / series.iloc[0]) ** 4)
        series.iloc[1] = (series.iloc[0] + ((series.iloc[1] - series.iloc[0]) / denom))
        return series.iloc[1]
    mcg_cell = close[0:].rolling(2, min_periods=2).apply(mcg_, raw=False)
    mcg_ds = close[:1].append(mcg_cell[1:])

Args:
    close (pd.Series): Series of 'close's
    length (int): Indicator's period.  Default: 10
    offset (int): Number of periods to offset the result.  Default: 0
    c (float): Multiplier for the denominator, sometimes set to 0.6. Default: 1

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""