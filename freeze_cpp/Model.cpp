#include <iostream>
#include <torch/script.h>
#include "Model.hpp"
#include "EvalJNI.h"
#define INPUT_BATCH_SIZE 1
//#define INPUT_SEQUENCE_SIZE 7
//#define INPUT_ELEMENT_SIZE 5
#define INPUT_ELEMENT_SIZE 3
//#define OUTPUT_SIZE 1
#define OUTPUT_SIZE 3
using namespace std;

namespace pytorch {
    Model::Model () {}
    Model::Model (const char* modelName) {
        this -> module = torch::jit::load(modelName);
    }
    Model::~Model () {}
    vector<float> Model::predict (vector<float> x) {
        //at::Tensor inputVector = torch::from_blob(&x[0], {INPUT_BATCH_SIZE, INPUT_SEQUENCE_SIZE, INPUT_ELEMENT_SIZE}, at::kFloat).clone();
        at::Tensor inputVector = torch::from_blob(&x[0], {INPUT_BATCH_SIZE, INPUT_ELEMENT_SIZE}, at::kFloat).clone();
        vector<torch::jit::IValue> inputTensor;
        inputTensor.push_back(inputVector);
        at::Tensor outputTensor = this -> module -> forward(inputTensor).toTensor();
        vector<float> outputVector(outputTensor.data<float>(), outputTensor.data<float>() + outputTensor.numel());
        return outputVector;
    }

    Eval::Eval () {}
    Eval::~Eval () {}
    long Eval::loadModel (const char* modelName) {
        Model* pModel = new Model(modelName);
        return long (pModel);
    }
    float* Eval::evaluate(long pModel, float* x) {
        //vector<float> vectorX (x, x + INPUT_BATCH_SIZE * INPUT_SEQUENCE_SIZE * INPUT_ELEMENT_SIZE);
        vector<float> vectorX (x, x + INPUT_BATCH_SIZE * INPUT_ELEMENT_SIZE);
        vector<float> vectorY = ((Model*)pModel) -> Model::predict(vectorX);
        static float y[OUTPUT_SIZE];
        for (int i = 0; i < OUTPUT_SIZE; ++i) {
            y[i] = vectorY[i];
        }
        return y;
    }
}

JNIEXPORT jlong JNICALL Java_EvalJNI_loadModel
  (JNIEnv * env, jobject thisObj, jstring modelName) {
  const char* modelNameString = env -> GetStringUTFChars(modelName, 0);
  pytorch::Eval eval = pytorch::Eval();
  long pModel = eval.loadModel(modelNameString);
  env -> ReleaseStringUTFChars(modelName, modelNameString);
  return pModel;
}

JNIEXPORT jfloatArray JNICALL Java_EvalJNI_evaluate
  (JNIEnv * env, jobject thisObj, jlong pModel, jfloatArray x) {
    jfloatArray result = env -> NewFloatArray(OUTPUT_SIZE);
    jfloat* jX = env -> GetFloatArrayElements(x, 0);

    pytorch::Eval eval = pytorch::Eval();
    float* y = eval.evaluate(pModel, jX);

    env -> ReleaseFloatArrayElements(x, jX, 0);
    env -> SetFloatArrayRegion(result, 0, OUTPUT_SIZE, y);
    return result;
}


int main(int argc, const char* argv[]) {
    if (argc != 2) {
        cerr << "argument mismatched\n";
        return -1;
    }

    pytorch::Model model = pytorch::Model("../../train_python/trace_model.pth");
    vector<float> vectorX;
    //for (int i = 0; i < INPUT_BATCH_SIZE * INPUT_SEQUENCE_SIZE * INPUT_ELEMENT_SIZE; ++i) {
    for (int i = 0; i < INPUT_BATCH_SIZE * INPUT_ELEMENT_SIZE; ++i) {
	    vectorX.push_back(i + 1);
    }
    vector<float> vectorY = model.predict(vectorX);
    cout << "model prediction" << endl;
    cout << vectorY << endl;

    pytorch::Eval eval = pytorch::Eval();
    long loadModel = eval.loadModel("../../train_python/trace_model.pth");
    float* x = &vectorX[0];
    float* y = eval.evaluate(loadModel, x);
    cout << "external evaluation" << endl;
    for (int i = 0; i < OUTPUT_SIZE; ++i) {
    	cout << y[i] << " " << endl;
    }
}
