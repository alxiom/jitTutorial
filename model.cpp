#include <iostream>
#include <memory>
#include <torch/script.h>
#include "model.hpp"

namespace traced {
    Model::Model () {}
    Model::Model (const char* modelName) {
        this->module = torch::jit::load(modelName);
    }
    Model::~Model () {}
    std::vector<float> Model::predict (std::vector<std::vector<float>> X) {
        at::Tensor inputVector = torch::from_blob(&X[0][0], {1, int (X[0].size())}, at::kFloat).clone();
        std::vector<torch::jit::IValue> inputTensor;
        inputTensor.push_back(inputVector);
        at::Tensor outputTensor = this->module->forward(inputTensor).toTensor();
        std::vector<float> outputVector(outputTensor.data<float>(), outputTensor.data<float>() + outputTensor.numel());
        return outputVector;
    }
}


int main(int argc, const char* argv[]) {
    if (argc != 2) {
        std::cerr << "argument mismatched\n";
        return -1;
    }

    traced::Model model = traced::Model("../traced_model.pth");
    std::vector<std::vector<float>> x = {{1, 1, 1}};
    std::cout << model.predict(x) << std::endl;
}