import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from icecream import ic
import dpcentre as dp


def func1():
    pass
    raw_data = pd.read_csv('../BrightRed1_1000ms.csv')
    data = dp.Data('bright red', raw_data)
    # ic(data.df)
    data.crop.by_x([43, 43.7])
    # data.crop.by_x([43, 43.7])
    # ic(data.df)
    # ic(cropped_data.df)
    # return mask, datah


def func2():
    raw_data = pd.read_csv('../BrightRed1_1000ms.csv')
    raw_data = raw_data.apply(pd.to_numeric, errors='coerce')
    # ic(raw_data)
    x = raw_data.iloc[:, 0]
    # ic(x)
    mask = (x >= 43) & (x <= 43.7)
    # mask = (raw_data.iloc[:, 0] >= 43 )& (raw_data.iloc[:, 0] <= 43.7)
    # ic(mask)
    raw_data = raw_data.loc[mask]
    ic(raw_data)
    return mask, raw_data


if __name__ == '__main__':
    func1()
    func2()

    # a0, a1 = func1()
    # b0, b1 = func2()
    # ic(a0 == b0)
    # ic(a1.equals(b1))
