#include "ModelJNI.h"
//#include "model.hpp"

JNIEXPORT jfloatArray JNICALL Java_ModelJNI_floatArrayMethod
(JNIEnv* env, jobject obj, jfloatArray x) {
    //jfloat* body = env->GetFloatArrayElements(x, 0);
    //traced::Model model = traced::Model("traced_model.pth");
    //std::vector result = model.predict(body)
    //env->ReleaseFloatArrayElements(x, body, model, 0);
    return x;
}
