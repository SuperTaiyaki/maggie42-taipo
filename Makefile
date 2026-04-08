# rsync would be better but ehhhh

BOARD = $(shell cat /mnt/sda1/BOARD)

switch:
ifeq ($(BOARD), gherkin)
	echo "Building Gherkin"
	make gherkin
else ifeq ($(BOARD), onthe17)
	echo "Building OnThe17"
	make onthe17
else ifeq ($(BOARD), handyman)
	echo "Building handyman"
	make handyman
else ifeq ($(BOARD), writer)
	echo "Building writer"
	make writer
else ifeq ($(BOARD), keyer)
	echo "Building keyer"
	make keyer
else ifeq ($(BOARD), maggie-r)
	echo "Building maggie right"
	echo "DISABLED"
	exit 1
	# REscue the files first
	make maggie-r
else
	echo "Building maggie"
	make maggie
endif

# mpy-cross: https://adafruit-circuit-python.s3.amazonaws.com/index.html?prefix=bin/mpy-cross/
MPY=../mpy-cross-linux-amd64-10.1.4.static

%.mpy: %.py
	$(MPY) -o $@ $<

clean:
	rm *.mpy

maggie: thicksplit.mpy synchronousscanner.mpy cykey.mpy jackdaw.mpy jackdaw_rules.mpy geminipr.mpy taipo.mpy dvp.mpy
	cp code.py /mnt/sda1/code.py
	cp $^  /mnt/sda1/ && sync

maggie-r:
	cp maggie-right.py /mnt/sda1/code.py
	cp thicksplit.py synchronousscanner.py cykey.py /mnt/sda1/ && sync

gherkin: code_gherkin.py cykey.mpy jackdaw.mpy jackdaw_rules.mpy synchronousscanner.mpy dvp.mpy
	cp code_gherkin.py /mnt/sda1/code.py
	cp $^ /mnt/sda1/ && sync

onthe17: pwm3360.mpy cykey.mpy jackdaw.mpy jackdaw_rules.mpy synchronousscanner.mpy dvp.mpy rgb_seventeen.mpy
	cp code_seventeen.py /mnt/sda1/code.py
	cp $^ /mnt/sda1/ && sync

handyman: cykey.mpy jackdaw.mpy geminipr.mpy taipo.mpy dvp.mpy 
	cp code-handyman.py /mnt/sda1/code.py
	cp $^ /mnt/sda1/ && sync

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
kmk:
	./mpy_tree.sh
	rsync kmk_mpy /mnt/sda1/kmk

all: switch
