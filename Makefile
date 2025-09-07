# rsync would be better but ehhhh
install:
	cp taipo.py code.py /mnt/sda1/ && sync

term:
	picocom /dev/ttyACM0

