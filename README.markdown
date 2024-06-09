# Barkalyzer

![image](./sample-plot.png)

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
./barkalyzer.py barks.mp4
```

## Debugging

Security cameras (e.g. Intelbras like mine) can be probed with `ffprobe` from your `ffmpeg` installation and streamed to a file. Password is set by you and IP is from your local network. Username and streaming path are hardcoded.

```
ffmpeg -i "rtsp://admin:password@192.168.x.y:554/cam/realmonitor?channel=1&subtype=0 -vcodec copy output.mp4"
```

You can then process `output.mp4` with Barkalyzer.
