import numpy as np


def minmax_scaler(data):
    numerator = data - np.min(data, 0)
    denominator = np.max(data, 0) - np.min(data, 0)
    return numerator / (denominator + 1e-7)


def build_dataset(time_series, seq_len):
    data_x = []
    data_y = []
    for j in range(0, len(time_series) - seq_len):
        _x = time_series[j:j + seq_len, :]
        _y = time_series[j + seq_len, [-1]]  # Next close price
        data_x.append(_x)
        data_y.append(_y)
    return np.array(data_x), np.array(data_y)
