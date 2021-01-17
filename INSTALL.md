# Installation software (macOS)

* detecting faces: detectron2
* encoding faces: face_recognition
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
brew install python3

brew link python3

brew upgrade python3

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
* install python libraries: `pip install numpy scipy matplotlib scikit-image scikit-learn ipython pandas`
* deactivate virtual environment: `deactivate`
* install openCV: `brew install opencv`
* configure python (check python version first):
  
  ```bash
  echo /usr/local/opt/opencv/lib/python3.6/site-packages >> usr/local/lib/python3.6/site-packages/opencv3.pth
  ```

* link OpenCV with virtual environment (check python version):
  
  ```bash
  find /usr/local/opt/opencv3/lib/ -name cv2*.so`
  cd ~/.virtualenvs/FAME/lib/python3.6/site-packages/
  ln -s /usr/local/opt/opencv3/lib/python3.6/site-packages/cv2.cpython-36m-darwin.so cv2.so
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
CC=clang XXX=clang++ pip install git+https://github.com/facebookresearch/detectron2.git
```

## face_recognition

Activate the virtual environment: `workon FAME`

### requirements

* dlib:
  
  ```bash
  git clone https://github.com/davisking/dlib.git && cd dlib
  python3 setup.py install
  ```

* cmake: `brew install cmake`

### installation

```bash
pip3 install face_recognition
```

## fuzzywuzzy

```bash
pip3 install fuzzywuzzy
```

## UMAP

Activate the virtual environment: `workon FAME`

```bash
pip install umap-learn
pip install umap-learn[plot]
```

## HDBSCAN

Activate the virtual environment: `workon FAME`

```bash
pip install hdbscan
```

## other

Activate the virtual environment: `workon FAME`

```bash
pip install datashader
pip install bokeh
pip install holoviews
pip install imutils
pip install python-Levenshtein
```
