#include <iostream>
#include <torch/script.h>
#include "Model.hpp"
#include "EvalJNI.h"
#define INPUT_SIZE 3
#define OUTPUT_SIZE 5

namespace pytorch {
    Model::Model () {}
    Model::Model (const char* modelName) {
        this -> module = torch::jit::load(modelName);
    }
    Model::~Model () {}
    std::vector<float> Model::predict (std::vector<float> x) {
        std::vector<std::vector<float>> xTensor;
        xTensor.push_back(x);
        at::Tensor inputVector = torch::from_blob(&xTensor[0][0], {1, INPUT_SIZE}, at::kFloat).clone();
        std::vector<torch::jit::IValue> inputTensor;
        inputTensor.push_back(inputVector);
        at::Tensor outputTensor = this -> module -> forward(inputTensor).toTensor();
        std::vector<float> outputVector(outputTensor.data<float>(), outputTensor.data<float>() + outputTensor.numel());
        return outputVector;
    }

    Eval::Eval () {}
    Eval::~Eval () {}
    long Eval::loadModel (const char* modelName) {
        Model* pModel = new Model(modelName);
        return long (pModel);
    }
    float* Eval::evaluate(long pModel, float* x) {
        std::vector<float> vectorX (x, x + INPUT_SIZE);
        std::vector<float> vectorY = ((Model*)pModel) -> Model::predict(vectorX);
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
        std::cerr << "argument mismatched\n";
        return -1;
    }

    pytorch::Model model = pytorch::Model("../trace_model.pth");
    std::vector<float> vectorX = {1.0, 1.0, 1.0};
    std::vector<float> vectorY = model.predict(vectorX);
    std::cout << "model prediction" << std::endl;
    std::cout << vectorY << std::endl;

    pytorch::Eval eval = pytorch::Eval();
    long loadModel = eval.loadModel("../trace_model.pth");
    float* x = &vectorX[0];
    float* y = eval.evaluate(loadModel, x);
    std::cout << "external evaluation" << std::endl;
    std::cout << y[0] << " " << y[1] << " " << y[2] << " " << y[3] << " " << y[4] << std::endl;
}