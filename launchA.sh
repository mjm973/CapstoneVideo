trap "kill 0" EXIT

python3 server.py &
python3 keyhole.py --host 10.225.47.90 --path /Volumes/USB/key.txt &
python3 relay.py -m --thost 10.225.47.90 --tport 8888 --mport 8888 &
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --kiosk 10.225.47.90:5000 &

wait
