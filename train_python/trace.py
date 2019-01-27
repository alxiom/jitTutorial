import torch
import model
import config
import numpy as np


class Trace:

    def __init__(self):
        super(Trace, self).__init__()
        seq_length = config.seq_length
        data_dim = config.data_dim
        hidden_dim = config.hidden_dim
        output_dim = config.output_dim

        load_net = model.Net(data_dim, hidden_dim, output_dim, 1)
        tracer = torch.Tensor(np.ones((1, seq_length, data_dim))).float()
        traced_net = torch.jit.trace(load_net, tracer)

        print(load_net(tracer))
        print(traced_net(tracer))

        print("tracing model...")
        traced_net.save("trace_model.pth")
        print("done")


if __name__ == '__main__':
    Trace()
