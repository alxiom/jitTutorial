# PyTorch JIT

## Requirements
+ cmake == 3.13.3
+ scala == 2.12.8
+ java == 1.8.0

## Preparation
1. Upgrade PyTorch
```markdown
$ pip install --upgrade torch
```
2. Install requirements (Mac)
```markdown
$ brew upgrade
$ brew install scala
$ brew install cmake
$ brew install wget
```
3. Download libtorch
```markdown
$ wget https://download.pytorch.org/libtorch/cpu/libtorch-macos-latest.zip
$ unzip libtorch-macos-latest.zip
$ mv libtorch /path/to/project/write_python
$ rm libtorch-macos-latest.zip
```
4. Install mkl-ml library
```markdown
$ wget https://github.com/intel/mkl-dnn/releases/download/v0.17.2/mklml_mac_2019.0.1.20181227.tgz
$ tar -zxvf mklml_mac_2019.0.1.20181227.tgz
$ mv mklml_mac_2019.0.1.20181227/lib/* /path/to/project/write_python/libtorch/lib/
$ rm -rf mklml_mac_2019.0.1.20181227
$ rm mklml_mac_2019.0.1.20181227.tgz
```

## Tracing (in write_python directory)
1. make and training model
2. add tracing code at ```model.py```
3. write cpp code at ```model.cpp, model.hpp```
4. tracing model by execution
```markdown
$ python model.py
```

## build C++ code (in write_python directory)
1. run cmake
```markdown
$ mkdir build
$ cd build
$ cmake -DCMAKE_PREFIX_PATH=/path/to/project/libtorch ..
$ make
$ ./model sample-input
```

## make JNI script (in read_scala directory)
1. make JNI scala code ```ModelJNI.scala```
2. compile
```markdown
$ cd /path/to/project/read_scala
$ sbt compile
```
3. create java header (Mac)
```markdown
$ cd target/scala-2.12/classes
$ javah -cp /usr/local/Cellar/scala/2.12.8/libexec/lib/scala-library.jar:. EvalJNI
$ mv EvalJNI.h ../../../../write_python
```
4. copy model trace, header and library
```markdown
$ cd ../../../../
$ cp write_python/traced_model.pth read_scala/src/main/scala
$ cp write_python/model.hpp read_scala/src/main/scala
$ cp write_python/build/libModel.dylib read_scala/lib
```
5. make C++ script ```ModelJNI.cpp```
6. make dylib file (Mac)
```markdown
$ mv libModelJNI.so ../../../lib
```
