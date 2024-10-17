import pandas as pd
from typing import Dict, List, Tuple
import math
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from scipy import optimize

from utilities import avg_in_region, filter_high_low


def plot_attenuation_objects(
        df_high: pd.DataFrame,
        df_low: pd.DataFrame,
        objects: Dict[str, float],
        ref_left: float,
        ref_right: float
) -> None:
    print("Drawing aggregated high-low plot of regions of interest")
    ref_high = avg_in_region(df_high, ref_left, ref_right)
    ref_low = avg_in_region(df_low, ref_left, ref_right)

    x_vals = [calc_attenuation(df_low, ref_low, obj['left'], obj['right']) for obj in objects]
    y_vals = [calc_attenuation(df_high, ref_high, obj['left'], obj['right']) for obj in objects]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.scatter(x_vals, y_vals)
    for i, obj in enumerate(objects):
        ax.annotate(obj['name'], (x_vals[i]+0.04, y_vals[i]+0.04))
    plt.xlabel("-ln(transmission) low")
    plt.ylabel("-ln(transmission) high")


def power_law(x, a, b):
    return a*np.power(x, b)


def plot_attenuation_point_cloud(
        df_high: pd.DataFrame,
        df_low: pd.DataFrame,
        ref_left: float,
        ref_right: float,
        regions_of_interest: List[Tuple[float, float, str, str]] = None,
        continuously_colour: bool = False,
        xy_filter: Dict[str, float] = None,
        kimberite_fit_range: Tuple[float, float] = None
) -> None:

    print("Getting unattenuated reference values")
    ref_high = avg_in_region(df_high, ref_left, ref_right)
    ref_low = avg_in_region(df_low, ref_left, ref_right)
    print(ref_high,ref_low)
    if xy_filter:
        df_high, df_low = filter_high_low(df_high, df_low, xy_filter)

    print("Taking negative log of transmission")
    df_high['att'] = -np.log(df_high['val'] / ref_high)
    df_low['att'] = -np.log(df_low['val'] / ref_low)

    #df_high['att'] = df_high['val'] / ref_high
    #df_low['att'] = df_low['val'] / ref_low

    fig, ax = plt.subplots(figsize=(10, 5))

    x_data = df_low['att']
    y_data = df_high['att']

    if regions_of_interest is None:
        if not continuously_colour:
            print("Drawing high-low point cloud")
            ax.scatter(x_data, y_data, s=8, color="b")
        else:
            print("Drawing continuously coloured high-low point cloud (purple->blue->green->yellow->red)")
            colors = cm.rainbow(np.linspace(0, 1, len(df_high)))
            for x, y, c in zip(x_data, y_data, colors):
                ax.scatter(x, y, s=5, color=c)

    else:
        print(f'Plotting points of interest within specified {len(regions_of_interest)} regions')
        for i, region in enumerate(regions_of_interest):
            (start, end, colour, label) = region

            df_high_sect = df_high[(df_high['x'] >= start) & (df_high['x'] <= end)]
            df_low_sect = df_low[(df_low['x'] >= start) & (df_low['x'] <= end)]
            ax.scatter(df_low_sect['att'], df_high_sect['att'], s=5, color=colour, label=label)

    if kimberite_fit_range:
        draw_kimberlite_locus(df_high, df_low, kimberite_fit_range, ax)
    ax.legend()
    ax.set_ylim(bottom=0)
    ax.set_xlim(left=0)
    plt.xlabel("Attenuation at low energy")
    plt.ylabel("Attenuation at high energy")
    plt.tight_layout()


def draw_kimberlite_locus(df_high: pd.DataFrame, df_low: pd.DataFrame, fit_range: Tuple[float, float], ax) -> None:
    x_fit = df_low.loc[(df_low.x >= fit_range[0]) & (df_low.x <= fit_range[1]), 'att']
    y_fit = df_high.loc[(df_high.x >= fit_range[0]) & (df_high.x <= fit_range[1]), 'att']

    print("Fitting power law")
    params, params_covariance = optimize.curve_fit(power_law, x_fit, y_fit, p0=[2, 1.5])
    x_plot_vals = np.linspace(0, ax.get_xlim()[1], 1000)
    y_plot_vals = power_law(x_plot_vals, params[0], params[1])

    ax.plot(x_plot_vals, y_plot_vals, label='Kimberlite locus', c=(0.4, 0.4, 0.8, 0.2), linewidth=5)
    print(f'Power law: y = {params[0]:.3f} * x^{params[1]:.3f}')


def calc_attenuation(df: pd.DataFrame, ref: float, left: float, right: float):
    av_val = avg_in_region(df, left, right)
    return -math.log(av_val / ref)
