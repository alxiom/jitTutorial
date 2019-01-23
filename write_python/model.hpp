#ifndef MODEL_H
#define MODEL_H

namespace pytorch {
    class Model {
        public:
            Model();
            Model(const char* modelName);
            ~Model();
            Model* loadModel(const char* modelName);
            std::shared_ptr<torch::jit::script::Module> module;
            std::vector<float> predict(std::vector<float> x);
            float* serve(long pModel, float* x, int vectorXSize);
    };
}

#endif