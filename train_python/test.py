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
        test_set = util.scale_minmax(test_set)
        test_x, test_y = util.build_dataset(test_set, seq_length)
        test_x_tensor = torch.Tensor(test_x).float()

        lstm_model = model.LSTMModel(data_dim, hidden_dim, output_dim, 1)
        lstm_model.load_state_dict(torch.load("save_model.pth"))
        lstm_model.eval()

        plt.plot(test_y)
        plt.plot(lstm_model(test_x_tensor).data.numpy())
        plt.legend(["original", "prediction"])
        plt.show()


if __name__ == '__main__':
    Test()
