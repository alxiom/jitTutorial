#ifndef Net_H
#define MODEL_H
//#include <iostream>
//#include <torch/script.h>

//namespace pytorch {
class Model {
    public:
        Model();
        Model(const char* modelName);
        ~Model();
        long loadModel(const char* modelName);
        std::shared_ptr<torch::jit::script::Module> module;
        std::vector<float> predict(std::vector<float> x);
        float* serve(long pModel, float* x, int vectorXSize);
};
//}

#endif