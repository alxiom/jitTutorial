import preprocess
import train
import trace
import test

print("preprocessing...")
preprocess.Preprocess()

print("training...")
train.Train()

print("tracing...")
trace.Trace()

print("testing...")
test.Test()

print("done")