#!/bin/sh
sudo apt update
sudo apt -y install bash-completion
curl -sSL https://install.python-poetry.org | python3 - --version 1.1.15
poetry completions bash >> ~/.bash_completion
