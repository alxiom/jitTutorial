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

        lstm_model = model.LSTMModel(data_dim, hidden_dim, output_dim, 1)
        lstm_model.load_state_dict(torch.load("save_model.pth"))
        lstm_model.eval()

        tracer = torch.Tensor(np.arange(1, seq_length * data_dim + 1).reshape((1, seq_length, data_dim))).float()
        print(tracer)
        trace_model = torch.jit.trace(lstm_model, tracer)

        print("model_output", lstm_model(tracer))
        print("trace_output", trace_model(tracer))

        print("tracing model...")
        trace_model.save("trace_model.pth")
        print("done")


if __name__ == '__main__':
    Trace()
