mkfifo pipe1
python3 corruption.py < pipe1 | python3 player.py > pipe1
