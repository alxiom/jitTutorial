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
        load_net.load_state_dict(torch.load("save_model.pth"))
        tracer = torch.Tensor(np.arange(1, seq_length * data_dim + 1).reshape((1, seq_length, data_dim))).float()
        print(tracer)
        traced_net = torch.jit.trace(load_net, tracer)

        print(load_net(tracer))
        print(traced_net(tracer))

        print("tracing model...")
        traced_net.save("trace_model.pth")
        print("done")


if __name__ == '__main__':
    Trace()
