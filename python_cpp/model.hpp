#ifndef MODEL_H
#define MODEL_H

namespace traced {
    class Model {
        public:
            Model();
            Model(const char* modelName);
            ~Model();
            std::shared_ptr<torch::jit::script::Module> module;
            std::vector<float> predict(std::vector<std::vector<float>> x);
    };
}

#endif