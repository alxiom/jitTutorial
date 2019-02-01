from torch import nn


class LSTMModel(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim, layers):
        super(LSTMModel, self).__init__()
        self.rnn = nn.LSTM(input_dim, hidden_dim, num_layers=layers, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim, bias=True)

    def forward(self, x):
        x, _status = self.rnn(x)
        x = self.fc(x[:, -1])
        return x
