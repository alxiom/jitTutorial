import preprocess
import train
import trace

print("preprocessing...")
preprocess.Preprocess()

print("training...")
train.Train()

print("tracing...")
trace.Trace()

print("done")

