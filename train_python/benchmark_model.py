import torch
from torch import nn
import numpy as np
import time


class BenchmarkModel(nn.Module):

    def __init__(self):
        super(BenchmarkModel, self).__init__()

        self.linear = nn.Sequential(
            nn.Linear(in_features=3, out_features=4096),
            # nn.BatchNorm1d(num_features=4096),
            nn.Tanh(),
            nn.Linear(in_features=4096, out_features=4096),
            # nn.BatchNorm1d(num_features=4096),
            nn.Tanh(),
            nn.Linear(in_features=4096, out_features=4096),
            # nn.BatchNorm1d(num_features=4096),
            nn.Tanh(),
            nn.Linear(in_features=4096, out_features=4096),
            # nn.BatchNorm1d(num_features=4096),
            nn.Tanh(),
            nn.Linear(in_features=4096, out_features=4096),
            # nn.BatchNorm1d(num_features=4096),
            nn.Tanh(),
            nn.Linear(in_features=4096, out_features=4096),
            # nn.BatchNorm1d(num_features=4096),
            nn.Tanh(),
            # nn.Linear(in_features=4096, out_features=4096),
            # nn.BatchNorm1d(num_features=4096),
            # nn.Tanh(),
            # nn.Linear(in_features=4096, out_features=4096),
            # nn.BatchNorm1d(num_features=4096),
            # nn.Tanh(),
            # nn.Linear(in_features=4096, out_features=4096),
            # nn.BatchNorm1d(num_features=4096),
            # nn.Tanh(),
            # nn.Linear(in_features=4096, out_features=4096),
            # nn.BatchNorm1d(num_features=4096),
            # nn.Tanh(),
            # nn.Linear(in_features=4096, out_features=4096),
            # nn.BatchNorm1d(num_features=4096),
            # nn.Tanh(),
            # nn.Linear(in_features=4096, out_features=4096),
            # nn.BatchNorm1d(num_features=4096),
            # nn.Tanh(),
            nn.Linear(in_features=4096, out_features=3)
        )

    def forward(self, inputs):
        return self.linear(inputs)


if __name__ == '__main__':
    load_model = BenchmarkModel()
    load_model.eval()
    tracer = torch.Tensor(np.random.random(size=(1, 3))).float()
    print(tracer)
    trace_model = torch.jit.trace(load_model, tracer)

    trace_output = trace_model(tracer)
    print("trace_output", trace_output)

    print("regular model elapsed time")
    s = time.time()
    load_model(tracer)
    t = time.time()
    print(t - s)

    print("traced model elapsed time")
    s = time.time()
    trace_model(tracer)
    t = time.time()
    print(t - s)

    trace_model.save("trace_model.pth")
