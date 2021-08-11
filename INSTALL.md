# Installation software (macOS)

* detecting faces: detectron2
* encoding faces: pyfacy
* visualisation: UMAP
* clustring: sklearn
* HDBSCAN

## general requirements

* Xcode Command Line Tools
* Homebrew
* Python3
* virtual environment
* OpenCV

### Xcode

```bash
xcode-select --install
```

### Homebrew

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Python3

```bash
brew update
brew install python@3.8 # 3.8 want 3.9 wordt nog niet door alle packages ondersteund.

brew link python@3.8

brew upgrade python@3.8

python3 --version
```

### Virtual environment

```bash
pip3 install virtualenv virtualenvwrapper
echo "# Virtual Environment Wrapper" >> ~/.bash_profile
echo "VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python3" >> ~/.bash_profile
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bash_profile
source ~/.bash_profile
```

### OpenCV

* create virtual environment: `mkvirtualenv FAME -p python3`
* activate virtual environment: `workon FAME`
* install python libraries: `pip3 install numpy scipy matplotlib scikit-image scikit-learn ipython pandas`
* deactivate virtual environment: `deactivate`
* install openCV: `brew install opencv`
* configure python (check python version first):
  
  ```bash
  echo /usr/local/opt/opencv/lib/python3.8/site-packages >> usr/local/lib/python3.8/site-packages/opencv3.pth
  ```

* link OpenCV with virtual environment (check python version):
  
  ```bash
  find /usr/local/opt/opencv3/lib/ -name cv2*.so`
  cd ~/.virtualenvs/FAME/lib/python3.8/site-packages/
  ln -s /usr/local/opt/opencv3/lib/python3.8/site-packages/cv2.cpython-36m-darwin.so cv2.so
  ```

* test OpenCV:
  
  ```python
  workon FAME
  ipython
  import cv2
  print(cv2.__version__)
  ```

## detectron2

Activate the virtual environment: `workon FAME`

### requirements

* pyyaml: `pip3 install pyyaml==5.1`
* torch and torchvision: `pip3 install torch torchvision`
* gcc and g++

### installation

```bash
CC=clang XXX=clang++ pip3 install git+https://github.com/facebookresearch/detectron2.git
```

## pyfacy

Activate the virtual environment: `workon FAME`

### requirements

* dlib: `pip3 install dlib`
* pyfacy models: `pip3 install pyfacy_dlib_models`
* imutils: `pip3 install imutils`
* numpy: `pip3 install numpy`
* scipy: `pip3 install scipy`
* scikit-learn: `pip3 install scikit-learn`

### installation

```bash
pip3 install pyfacy
```

## fuzzywuzzy

```bash
pip3 install fuzzywuzzy
```

## UMAP

Activate the virtual environment: `workon FAME`

```bash
pip3 install umap-learn
```

## HDBSCAN

Activate the virtual environment: `workon FAME`

```bash
pip3 install --user hdbscan
```

## other

Activate the virtual environment: `workon FAME`

```bash
pip3 install datashader
pip3 install bokeh
pip3 install holoviews
pip3 install python-Levenshtein
```
