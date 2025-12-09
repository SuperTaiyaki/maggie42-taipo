# rsync would be better but ehhhh

BOARD = $(shell cat /mnt/sda1/BOARD)

switch:
ifeq ($(BOARD), gherkin)
	echo "Building Gherkin"
	make gherkin
else ifeq ($(BOARD), handyman)
	echo "Building handyman"
	make handyman
else ifeq ($(BOARD), writer)
	echo "Building writer"
	make writer
else ifeq ($(BOARD), keyer)
	echo "Building keyer"
	make keyer
else
	echo "Building maggie"
	make maggie
endif

maggie:
	cp thicksplit.py cykey.py jackdaw.py jackdaw_rules.py geminipr.py taipo.py dvp.py code.py /mnt/sda1/ && sync

gherkin:
	cp code_gherkin.py /mnt/sda1/code.py
	cp cykey.py jackdaw.py jackdaw_rules.py geminipr.py taipo.py dvp.py /mnt/sda1/ && sync

handyman:
	cp code-handyman.py /mnt/sda1/code.py
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

all: switch
