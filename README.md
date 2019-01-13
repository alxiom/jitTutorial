# PyTorch JIT

## Preparation
1. Upgrade PyTorch
```markdown
$ pip install --upgrade torch
```
2. Upgrade cmake
```markdown
$ brew upgrade
$ brew install cmake
```
3. Download libtorch
```markdown
https://download.pytorch.org/libtorch/cpu/libtorch-macos-latest.zip
$ unzip libtorch-macos-latest.zip
$ mv libtorch /path/to/project
```
4. Install mkl-ml library
```markdown
https://github.com/intel/mkl-dnn/releases (version : mklml_mac_2019.0.1.20181227.tgz)
$ tar -zxvf mklml_mac_2019.0.1.20181227.tgz
$ mv mklml_mac_2019.0.1.20181227/lib/* /path/to/project/libtorch/lib/
```

## Tracing
1. add tracing code ```model.py```
2. write cpp code ```model.cpp```
3. write CMakeLists ```CMakeLists.txt```
4. tracing code
```markdown
$ python model.py
```

## build C++ code
1. run cmake
```markdown
$ mkdir build
$ cd build
$ cmake -DCMAKE_PREFIX_PATH=/path/to/project/libtorch ..
$ make
$ ./model sample-input
```
