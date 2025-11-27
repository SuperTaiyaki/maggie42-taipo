# rsync would be better but ehhhh
install:
	test -f /mnt/sda1/WRITER && echo "ERROR: Wrong board" && exit 1 || true
	cp thicksplit.py cykey.py jackdaw.py geminipr.py taipo.py dvp.py code.py /mnt/sda1/ && sync

gherkin:
	cp code_gherkin.py /mnt/sda1/code.py
	cp cykey.py jackdaw.py geminipr.py taipo.py dvp.py /mnt/sda1/ && sync

writer:
	cp code-board.py /mnt/sda1/code.py
	cp writer.py cykey.py dvorak.py wordlist.py dvp.py /mnt/sda1/ && sync

keyer:
	cp code-keyer.py /mnt/sda1/code.py
	cp cykey.py dvp.py /mnt/sda1/ && sync

term:
	picocom /dev/ttyACM0

keymap:
	./render_cykey
# TODO: adafruit libraries as required

