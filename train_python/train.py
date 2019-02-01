import torch
import torch.optim as optim
import numpy as np
import config
import model
import util


class Train:

    def __init__(self):
        super(Train, self).__init__()
        torch.manual_seed(42)

        seq_length = config.seq_length
        data_dim = config.data_dim
        hidden_dim = config.hidden_dim
        output_dim = config.output_dim
        learning_rate = config.learning_rate
        iterations = config.iterations

        train_set = np.loadtxt("stock_daily_train.csv", delimiter=",")
        train_set = util.scale_minmax(train_set)
        train_x, train_y = util.build_dataset(train_set, seq_length)
        train_x_tensor = torch.Tensor(train_x).float()
        train_y_tensor = torch.Tensor(train_y).float()

        lstm_model = model.LSTMModel(data_dim, hidden_dim, output_dim, 1)
        criterion = torch.nn.MSELoss()
        optimizer = optim.Adam(lstm_model.parameters(), lr=learning_rate)

        lstm_model.train()
        for i in range(iterations):

            optimizer.zero_grad()
            outputs = lstm_model(train_x_tensor)
            loss = criterion(outputs, train_y_tensor)
            loss.backward()
            optimizer.step()

            if (i + 1) % 10 == 0:
                print("{:3d} {}".format(i + 1, loss.item()))
            if i + 1 == iterations:
                print("save model...")
                torch.save(lstm_model.state_dict(), "save_model.pth")
                print("done")


if __name__ == '__main__':
    Train()
