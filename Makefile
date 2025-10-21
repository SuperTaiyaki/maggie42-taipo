# rsync would be better but ehhhh
install:
	test -f /mnt/sda1/WRITER && echo "ERROR: Wrong board" && exit 1 || true
	cp cykey.py code.py /mnt/sda1/ && sync

writer:
	cp code-board.py /mnt/sda1/code.py
	cp writer.py cykey.py dvorak.py wordlist.py /mnt/sda1/ && sync

keyer:
	cp code-keyer.py /mnt/sda1/code.py
	cp cykey.py /mnt/sda1/ && sync

term:
	picocom /dev/ttyACM0

# TODO: adafruit libraries as required
