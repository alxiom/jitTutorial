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
        train_set = util.minmax_scaler(train_set)
        trainX, trainY = util.build_dataset(train_set, seq_length)
        trainX_tensor = torch.Tensor(trainX).float()
        trainY_tensor = torch.Tensor(trainY).float()

        net = model.Net(data_dim, hidden_dim, output_dim, 1)
        criterion = torch.nn.MSELoss()
        optimizer = optim.Adam(net.parameters(), lr=learning_rate)

        for i in range(iterations):

            optimizer.zero_grad()
            outputs = net(trainX_tensor)
            loss = criterion(outputs, trainY_tensor)
            loss.backward()
            optimizer.step()
            print(i + 1, loss.item())
            if i + 1 == iterations:
                print("save model...")
                torch.save(net.state_dict(), "save_model.pth")
                print("done")


if __name__ == '__main__':
    Train()
