#include <iostream>
#include <torch/script.h>
#include "model.hpp"
#define MAX_SIZE 256


namespace pytorch {
    Model::Model () {}

    Model::~Model () {}

    Model::Model (const char* modelName) {
        this -> module = torch::jit::load(modelName);
    }

    Model* Model::loadModel (const char* modelName) {
        Model* pModel = new Model(modelName);
        return pModel;
    }

    std::vector<float> Model::predict (std::vector<float> x) {
        std::vector<std::vector<float>> xTensor;
        xTensor.push_back(x);
        at::Tensor inputVector = torch::from_blob(&xTensor[0][0], {1, int (x.size())}, at::kFloat).clone();
        std::vector<torch::jit::IValue> inputTensor;
        inputTensor.push_back(inputVector);
        at::Tensor outputTensor = this -> module -> forward(inputTensor).toTensor();
        std::vector<float> outputVector(outputTensor.data<float>(), outputTensor.data<float>() + outputTensor.numel());
        return outputVector;
    }

    float* Model::serve(long pModel, float* x, int vectorXSize) {
        std::vector<float> vectorX (x, x + vectorXSize);
        std::vector<float> vectorY = ((Model*)pModel) -> predict(vectorX);
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

    pytorch::Model model = pytorch::Model("../traced_model.pth");
    std::vector<float> vectorX = {1.0, 1.0, 1.0};
    std::vector<float> vectorY = model.predict(vectorX);
    std::cout << vectorY << std::endl;

    long loadModel = long (model.loadModel("../traced_model.pth"));
    float* x = &vectorX[0];
    int xSize = vectorX.size();
    float* y = model.serve(loadModel, x, xSize);
    std::cout << y[0] << " " << y[1] << " " << y[2] << " " << y[3] << " " << y[4] << std::endl;
}
