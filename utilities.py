import pandas as pd
from typing import Tuple, Dict


def avg_in_region(df: pd.DataFrame, left: float, right: float) -> float:
    return df[(df['x'] >= left) & (df['x'] <= right)]['val'].mean()


def filter_high_low(df_high: pd.DataFrame, df_low: pd.DataFrame,
                    xy_filter: Dict[str, float]) -> Tuple[pd.DataFrame, pd.DataFrame]:

    print(f"Filtering points, x in ({xy_filter['x_low']}, {xy_filter['x_high']}), "
          f"y in ({xy_filter['y_low']}, {xy_filter['y_high']})")

    row_filter = (df_high.val >= xy_filter['y_low']) & (df_high.val <= xy_filter['y_high']) & \
                 (df_low.val >= xy_filter['y_low']) & (df_low.val <= xy_filter['y_high']) & \
                 (df_high.x >= xy_filter['x_low']) & (df_high.x <= xy_filter['x_high']) & \
                 (df_low.x >= xy_filter['x_low']) & (df_low.x <= xy_filter['x_high'])
    df_high = df_high[row_filter].copy()
    df_low = df_low[row_filter].copy()
    return df_high, df_low
