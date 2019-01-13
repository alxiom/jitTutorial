import torch
from torch import nn
import numpy as np


class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()

        self.linear = nn.Sequential(
            nn.Linear(in_features=3, out_features=100),
            nn.Linear(in_features=100, out_features=5)
        )

    def forward(self, inputs):
        return self.linear(inputs)


if __name__ == "__main__":
    model = Net()  # TODO : load trained model
    tracer = torch.Tensor(np.random.random((1, 3))).float()
    traced_net = torch.jit.trace(model, tracer)

    print(model(tracer))
    print(traced_net(tracer))

    traced_net.save("traced_model.pth")
