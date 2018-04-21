trap "kill 0" EXIT

python3 server.py -b &
python3 keyhole.py --host 10.225.99.83 --path /Volumes/USB/key.txt &
python3 relay.py -m --thost 10.225.99.83 --tport 8888 --mport 8888 &

wait
