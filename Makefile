# rsync would be better but ehhhh
install:
	cp cykey.py code.py /mnt/sda1/ && sync

term:
	picocom /dev/ttyACM0

