# PyTorch model tracing tutorial 
+ Using JIT compile support since PyTorch 1.0.0

## Requirements
+ python == 3.7.0
+ torch == 1.0.0
+ numpy == 1.16.0

## Preparation
1. Upgrade PyTorch
```markdown
pip install --upgrade pip
pip install --upgrade torch
pip install --upgrade numpy
```

## Tracing 
1. create and training a model in PyTorch
2. trace model by execute tracing (refer ```trace.py``` in ```main.py```)
```markdown
cd /path/to/project/trace_trained_RNN
python main.py
```
