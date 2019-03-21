# PyTorch model tracing tutorial 
+ Using JIT compile support since PyTorch 1.0.0

## Requirements
+ python == 3.7.0
+ torch == 1.0.0
+ numpy == 1.16.0

## Preparation
1. Upgrade PyTorch
```
pip install --upgrade pip
pip install --upgrade torch
pip install --upgrade numpy
```

## Tracing 
Refer ```trace_benchmark_DNN/benchmark.py``` or ```trace_trained_RNN/trace.py```

1. training a model in PyTorch
2. create a "tracer" which is an input tensor of the model
3. trace model by passing through the tracer to the model with ```torch.jit.trace(your_model, tracer)```

Overall process is executed by followings
```
git clone https://github.com/hyoungseok/jitTutorial.git
cd jitTutorial/trace_trained_RNN
python main.py
```
The traced file ```traced_model.pth``` will be created under the ```jitTutorial/trace_trained_RNN```

## Contributors
+ YongRae Jo (dreamgonfly@gmail.com)

## Author
+ Alex Kim (hyoungseok.k@gmail.com)
