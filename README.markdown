# Barkalyzer

## Setup

### macOS

Dependencies:

```
brew install pyenv pyenv-virtualenv
```

Local shell config in `~/.profile`:

```
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"

eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

Python stuff:

```
cd barkalyzer/

pyenv install 3.8.10
pyenv virtualenv 3.8.10 myenv
pyenv activate myenv

pyenv local myenv
pip install --upgrade pip
```

Requirements:

```
pip install -r requirements.txt
```

## Run

```
./barkalyzer.py
```