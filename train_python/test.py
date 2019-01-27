import torch
import numpy as np
import config
import model
import util
import matplotlib.pyplot as plt


class Test:

    def __init__(self):
        super(Test, self).__init__()
        seq_length = config.seq_length
        data_dim = config.data_dim
        hidden_dim = config.hidden_dim
        output_dim = config.output_dim

        test_set = np.loadtxt("stock_daily_test.csv", delimiter=",")
        test_set = util.minmax_scaler(test_set)
        test_x, test_y = util.build_dataset(test_set, seq_length)
        test_x_tensor = torch.Tensor(test_x).float()

        load_net = model.Net(data_dim, hidden_dim, output_dim, 1)
        load_net.load_state_dict(torch.load("save_model.pth"))

        plt.plot(test_y)
        plt.plot(load_net(test_x_tensor).data.numpy())
        plt.legend(["original", "prediction"])
        plt.show()


if __name__ == '__main__':
    Test()
