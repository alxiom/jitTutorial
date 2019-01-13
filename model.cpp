#include <iostream>
#include <memory>
#include <torch/script.h>

int main(int argc, const char* argv[]) {
    if (argc != 2) {
        std::cerr << "usage: model <input-vector>\n";
        return -1;
    }

    std::shared_ptr<torch::jit::script::Module> module = torch::jit::load("../traced_model.pth");

    std::vector<torch::jit::IValue> inputs;
    inputs.push_back(torch::ones({1, 3})); // TODO : make user input

    at::Tensor output = module->forward(inputs).toTensor();
    std::cout << output.slice(/*dim=*/1, /*start=*/0, /*end=*/5) << '\n';
}
