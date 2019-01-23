#include <iostream>
#include <memory>
#include <array>
#include <torch/script.h>
#include "model.hpp"

namespace traced {
    Model::Model () {}
    Model::Model (const char* modelName) {
        this->module = torch::jit::load(modelName);
    }
    Model::~Model () {}
    std::vector<float> Model::predict (std::vector<float> x) {
        std::vector<std::vector<float>> xTensor;
        xTensor.push_back(x);
        at::Tensor inputVector = torch::from_blob(&xTensor[0][0], {1, int (x.size())}, at::kFloat).clone();
        std::vector<torch::jit::IValue> inputTensor;
        inputTensor.push_back(inputVector);
        at::Tensor outputTensor = this->module->forward(inputTensor).toTensor();
        std::vector<float> outputVector(outputTensor.data<float>(), outputTensor.data<float>() + outputTensor.numel());
        return outputVector;
    }

    Eval::Eval () {}
    Eval::~Eval () {}
    Model* Eval::createModel (const char* modelName) {
        Model* pModel = new Model(modelName);
        return pModel;
    }
    float* Eval::evaluate(long pModel, float* x, int vectorLength) {
        std::vector<float> vectorX (x, x + vectorLength);
        std::vector<float> vectorY = ((Model*)pModel) -> predict(vectorX);
        std::cout << vectorY << std::endl;
        float* y = &vectorY[0];
        std::cout << y[0] << " " << y[1] << " " << y[2] << " " << y[3] << " " << y[4] << std::endl;
        return y;
    }
}


int main(int argc, const char* argv[]) {
    if (argc != 2) {
        std::cerr << "argument mismatched\n";
        return -1;
    }

//    traced::Model model = traced::Model("../traced_model.pth");
//    std::vector<float> x = {1, 1, 1};
//    std::cout << model.predict(x) << std::endl;

    traced::Eval eval = traced::Eval();
    long loadModel = long (eval.createModel("../traced_model.pth"));
//    std::cout << loadModel << std::endl;

    float y[] = {1.0, 1.0, 1.0};
    int vecLen = sizeof(y) / sizeof(*y);
    float prediction[5] = {0, 0, 0, 0, 0};
    prediction = eval.evaluate(loadModel, y, vecLen);
//    float a[] = {};
//    a = prediction
//    std::vector<float> vectorY (prediction, prediction + 5);
    std::cout << prediction << std::endl;
//    float* a = prediction;
//    std::cout << a[0] << std::endl;
//    std::cout << prediction[0] << prediction[1] << prediction[2] << prediction[3] << prediction[4] << std::endl;
//    std::cout << *(prediction + 2) << std::endl;
//    std::cout << prediction << std::endl;

}
