#include <iostream>
#include <memory>
#include <array>
#include <torch/script.h>
#include "model.hpp"
#define MAX_SIZE 256


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
    float* Eval::evaluate(long pModel, float* x, int vectorXSize) {
        std::vector<float> vectorX (x, x + vectorXSize);
        std::vector<float> vectorY = ((Model*)pModel) -> predict(vectorX);
        std::cout << vectorY << std::endl;
        static float* y;
        y = (float*) malloc(MAX_SIZE * sizeof(float));
        for (int i = 0; i < vectorY.size(); ++i) {
            y[i] = vectorY[i];
        }
        return y;
    }
}


int main(int argc, const char* argv[]) {
    if (argc != 2) {
        std::cerr << "argument mismatched\n";
        return -1;
    }

    traced::Model model = traced::Model("../traced_model.pth");
    std::vector<float> vectorX = {1.0, 1.0, 1.0};
    std::cout << model.predict(vectorX) << std::endl;

    traced::Eval eval = traced::Eval();
    long loadModel = long (eval.createModel("../traced_model.pth"));

    float* x = &vectorX[0];
    int xSize = vectorX.size();
    float* p = eval.evaluate(loadModel, x, xSize);
    std::cout << p[0] << " " << p[1] << " " << p[2] << " " << p[3] << " " << p[4] << std::endl;

}
