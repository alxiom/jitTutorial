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

        load_model = model.Net(data_dim, hidden_dim, output_dim, 1)
        load_model.load_state_dict(torch.load("save_model.pth"))
        tracer = torch.Tensor(np.arange(1, seq_length * data_dim + 1).reshape((1, seq_length, data_dim))).float()
        print(tracer)
        trace_model = torch.jit.trace(load_model, tracer)

        print(load_model(tracer))
        print(trace_model(tracer))

        print("tracing model...")
        trace_model.save("trace_model.pth")
        print("done")


if __name__ == '__main__':
    Trace()
