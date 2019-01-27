import config
import numpy as np


class Preprocess:

    def __init__(self):
        super(Preprocess, self).__init__()
        seq_length = config.seq_length
        data_path = config.data_path
        train_set_save_path = config.train_set_save_path
        test_set_save_path = config.test_set_save_path
        split_ratio = 0.7

        xy = np.loadtxt(data_path, delimiter=",")
        xy = xy[::-1]  # reverse order

        train_size = int(len(xy) * split_ratio)
        train_set = xy[0:train_size]
        test_set = xy[train_size - seq_length:]

        print("save train set...")
        np.savetxt(train_set_save_path, train_set, delimiter=",", encoding="utf-8")
        print("done")

        print("save test set...")
        np.savetxt(test_set_save_path, test_set, delimiter=",", encoding="utf-8")
        print("done")


if __name__ == '__main__':
    Preprocess()
