trap "kill 0" EXIT

/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew install python
pip3 install flask
pip3 install requests
pip3 install opencv-python==3.3.0.10
pip3 install pyserial
pip3 install python-osc
sudo systemsetup -setremotelogin on

wait
