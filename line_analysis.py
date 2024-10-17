import pandas as pd
import matplotlib.pyplot as plt
from attenuation_plot import plot_attenuation_objects, plot_attenuation_point_cloud
from typing import Tuple


def average_data(df_dat: pd.DataFrame,) -> pd.DataFrame:
    df_agg = df_dat.agg({col: 'mean' for col in df_dat.columns})

    df_agg = df_agg.reset_index(drop=True)
    df_agg = df_agg.reset_index(drop=False)
    df_agg.columns = ['pixel', 'val']
    df_agg['x'] = df_agg['pixel'] * 1.6
    df_agg = df_agg.drop('pixel', axis=1)

    return df_agg


def get_high_low(filename: str, num_boards) -> Tuple[pd.DataFrame, pd.DataFrame]:
    print("Reading in data")
    df_in = pd.read_csv(filename)
    print("Splitting high and low energy")
    df_h = df_in.loc[:, 'D1':f'D{64*num_boards}']
    df_l = df_in.loc[:, f'D{64*num_boards + 1}':f'D{128*num_boards}']

    print("Averaging rows")
    df_low_agg = average_data(df_l)
    df_high_agg = average_data(df_h)
    return df_high_agg, df_low_agg


def plot_line(df_high: pd.DataFrame, df_low: pd.DataFrame, plot_title: str) -> None:
    fig, ax = plt.subplots(figsize=(10, 5))
    x_max = df_low['x'].max()

    print("Drawing step plots of high and low energy")
    df_high = df_high.reset_index()
    df_low = df_low.reset_index()

    ax.step(x=df_low['x'], y=df_low['val'], linewidth=1)
    ax.step(x=df_high['x'], y=df_high['val'], linewidth=1)

    # flips x
    # ax.step(x=x_max - df_low['x'], y=df_low['val'], linewidth=1)
    # ax.step(x=x_max - df_high['x'], y=df_high['val'], linewidth=1)


    ax.legend(["low", "high"])
    ax.set_xlabel("x along detector (mm)")
    ax.set_ylabel("Pixel intensity")
    ax.set_title(plot_title)
    ax.set_xlim(left=0, right=x_max)
    ax.set_ylim(bottom=0)
    plt.tight_layout()


def interpolate_spikes(df: pd.DataFrame) -> pd.DataFrame:
    print("Interpolating spikes")
    threshold = 0.95
    df['interpolated'] = df['val'].rolling(3, center=True).mean()*3/2 - df['val']/2
    row_filter = df['val'] < df['interpolated'] * threshold
    df.loc[row_filter, 'val'] = df.loc[row_filter, 'interpolated']
    return df.drop('interpolated', axis=1)


def plot_0():
    df_high_dat, df_low_dat = get_high_low('/Users/gideon/Documents/Gem-XRT/W_data1/wedge_1_mid.csv', 9)
    objects = [
        {'left': 124., 'right': 150., 'name': 'kimb1'},
        {'left': 350., 'right': 430., 'name': 'kimb2'},
        {'left': 585., 'right': 595., 'name': 'bolt'},
        {'left': 667., 'right': 675., 'name': 'diamond'},
        {'left': 743., 'right': 751., 'name': 'copper'},
    ]
    ref_left, ref_right = 780, 900

    plot_line(df_high_dat, df_low_dat, '140kV kimb, bolt diamond and copper')
    plot_attenuation_objects(df_high_dat, df_low_dat, objects, ref_left, ref_right)

    plt.show()


def plot_1():
    df_high_dat, df_low_dat = get_high_low('/Users/gideon/Documents/Gem-XRT/W_data1/wedge_1_mid.csv', 9)
    objects = [
        {'left': 124., 'right': 150., 'name': 'kimb1'},
        {'left': 350., 'right': 430., 'name': 'kimb2'},
        {'left': 585., 'right': 595., 'name': 'bolt'},
        {'left': 667., 'right': 675., 'name': 'diamond'},
        {'left': 743., 'right': 751., 'name': 'copper'},
    ]
    ref_left, ref_right = 780, 900

    xy_filter = {
        'x_low': 105,
        'x_high': 800,
        'y_low': 3000,
        'y_high': 47000,
    }

    plot_line(df_high_dat, df_low_dat, '140kV kimb, bolt diamond and copper')
    # plot_attenuation_objects(df_high_dat, df_low_dat, objects, ref_left, ref_right)
    plot_attenuation_point_cloud(df_high_dat, df_low_dat, ref_left, ref_right,
                                 continuously_colour=True, xy_filter=xy_filter)


    plt.show()


def plot_2():
    df_high_dat, df_low_dat = get_high_low('/Users/gideon/Documents/Gem-XRT/W_data1/wedge_1_mid.csv', 10)
    objects = [
        {'left': 91., 'right': 128., 'name': 'kimb1'},
        {'left': 206., 'right': 308., 'name': 'kimb2'},
        {'left': 351., 'right': 417., 'name': 'kimb3'},
        {'left': 431., 'right': 464., 'name': 'kimb4'},
        {'left': 552., 'right': 600., 'name': 'kimb5'},
        {'left': 680., 'right': 684., 'name': 'diamond1'},
        {'left': 757., 'right': 762., 'name': 'diamond2'},
    ]
    ref_left, ref_right = 799, 907

    plot_line(df_high_dat, df_low_dat, '140kV, kimberlite plus two diamonds')
    plot_attenuation_objects(df_high_dat, df_low_dat, objects, ref_left, ref_right)

    plt.show()


def plot_3():
    #df_high_dat, df_low_dat = get_high_low('../data/25052021/150kV_3mA_350us_different_pC.csv', 10)
    #df_high_dat, df_low_dat = get_high_low('../data/27052021/wedge_1_mid_left.csv', 10)
    #df_high_dat, df_low_dat = get_high_low('../data/27052021/wedge__19_left.csv', 10)
    df_high_dat, df_low_dat = get_high_low('/Users/gideon/Documents/Gem-XRT/W_data1/wedge_1_mid.csv', 10)
    #df_high_dat, df_low_dat = get_high_low('../data/28052021/wedge__FK_1_FK_2_30mm_10mmDiamond_Left_FK_3_10mm_6mmDiamond_Right_150KV.csv', 10)
    df_high_dat = interpolate_spikes(df_high_dat)
    objects = [
        {'left': 87., 'right': 122., 'name': 'kimb1'},
        {'left': 211., 'right': 300., 'name': 'kimb2'},
        {'left': 346., 'right': 418., 'name': 'kimb3'},
        {'left': 431., 'right': 467., 'name': 'kimb4'},
        {'left': 560., 'right': 595., 'name': 'kimb5'},
        {'left': 682., 'right': 684., 'name': 'diamond1'},
        {'left': 757., 'right': 760., 'name': 'diamond2'},
    ]
    ref_left, ref_right = 900, 950
    #ref_left, ref_right = 799, 907

    plot_line(df_high_dat, df_low_dat, '150kV, kimberlite plus two diamonds')
    #plot_attenuation_objects(df_high_dat, df_low_dat, objects, ref_left, ref_right)

    regions_of_interest = [
        (195, 326, 'tab:purple', '22mm kimberlite'),
        (327, 481, 'tab:green', '12mm kimberlite'),
        (503, 640, 'tab:blue', 'Wedge 2mm to 10mm kimberlite'),
        (671, 690, 'tab:red', 'Diamond 5mm'),
        (745, 777, 'tab:orange', 'Diamond 10mm')
    ]

    xy_filter = {
        'x_low': 10, # was 205
        'x_high': 821, # was 800
        #'y_low': 1000, # was 3000,
        #'y_high': 5500, # was 47000,
        #'x_low': 205,
        #'x_high': 800,
        'y_low': 3000,
        'y_high': 47000,
    }

    #plot_attenuation_point_cloud(df_high_dat, df_low_dat, ref_left, ref_right,
    #                            regions_of_interest, xy_filter=xy_filter,
    #                            kimberite_fit_range=(xy_filter['x_low'], 645))
    plot_attenuation_point_cloud(df_high_dat, df_low_dat, ref_left, ref_right,
                                continuously_colour=True,
                                xy_filter=xy_filter,
                                #kimberite_fit_range=(xy_filter['x_low'], 645))
                                kimberite_fit_range=(xy_filter['x_low'], xy_filter['x_high']))
                                #kimberite_fit_range=(108,146 ))

    plt.show()


def plot_4():
    df_high_dat, df_low_dat = get_high_low('/Users/gideon/Documents/Gem-XRT/W_data1/wedge_1_mid.csv', 10)
    objects = [
        {'left': 91., 'right': 128., 'name': 'kimb1'},
        {'left': 206., 'right': 308., 'name': 'kimb2'},
        {'left': 351., 'right': 417., 'name': 'kimb3'},
        {'left': 431., 'right': 464., 'name': 'kimb4'},
        {'left': 552., 'right': 600., 'name': 'kimb5'},
        {'left': 680., 'right': 684., 'name': 'diamond1'},
        {'left': 757., 'right': 762., 'name': 'diamond2'},
    ]
    ref_left, ref_right = 799, 907

    plot_line(df_high_dat, df_low_dat, '80kV')
    plot_attenuation_objects(df_high_dat, df_low_dat, objects, ref_left, ref_right)

    plt.show()


def plot_5():
    file_names=['wedge_10_25.csv',  'wedge_16_7.csv', 'wedge_2_49.csv', 'wedge_8_31.csv', 'wedge__22_left.csv', 'wedge__40_left.csv',  'wedge_11_22.csv',  'wedge_17_4.csv', 'wedge_3_46.csv', 'wedge_9_28.csv', 'wedge__25_left.csv', 'wedge__43_left.csv',  'wedge_12_19.csv',  'wedge_1_49_left.csv',  'wedge_4_43.csv', 'wedge__10_left.csv', 'wedge__28_left.csv', 'wedge__4_left.csv',  'wedge_13_16.csv',  'wedge_1_mid.csv',  'wedge_5_40.csv', 'wedge__13_left.csv', 'wedge__31_left.csv', 'wedge__7_left.csv',  'wedge_14_13.csv',  'wedge_1_mid_left.csv', 'wedge_6_37.csv', 'wedge__16_left.csv', 'wedge__34_left.csv',  'wedge_15_10.csv',  'wedge_2_46_left.csv',  'wedge_7_34.csv', 'wedge__19_left.csv', 'wedge__37_left.csv']

    xy_filter = {
        'x_low': 205,
        'x_high': 800,
        'y_low': 3000,
        'y_high': 47000,
    }

    for file_name in file_names:
        df_high_dat, df_low_dat = get_high_low('../data/27052021/'+file_name, 10)
        df_high_dat = interpolate_spikes(df_high_dat)
        objects = [
        {'left': 1., 'right': 640., 'name':file_name },
        ]
        print("Now doing file" + file_name)
        ref_left, ref_right = 799, 907
        plot_line(df_high_dat, df_low_dat, '150kV, kimberlite wedge')
        plot_attenuation_point_cloud(df_high_dat, df_low_dat, ref_left, ref_right,
                                 continuously_colour=True,
                                 xy_filter=xy_filter,
                                 kimberite_fit_range=(xy_filter['x_low'], 645))
        plt.show()


plot_3()
