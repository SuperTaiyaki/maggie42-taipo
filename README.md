This the customized firmware for my keyboard.
The concept was a keyboard primarily for typing on the [Taipo]() 10-key layout, hence the 8 yellow keys. 
It's entirely usable with only the left or right half connected, with a full-layout mode for both halves.

(TODO: photo)

The board is a Studio Purring (Tamaroh) [Maggie42cs0](https://github.com/tamaroh/maggie42cs0), built from one of their commercial PCBs.
As per the design it's running on a pair of RP2040-zeros.
Because this board is meant for chording the main switches are light Kailh Sakers. After using it for a bit
it would have been fine to go even lighter.

Base firmware is KMK as of late August 2025; I don't see anything resembling a version number.

Taipo firmware is based on [dlip's package](https://github.com/dlip/chouchou/tree/main/firmware/kmk).
The version in that source tree is outdated and doesn't quite work with current KMK.

Modifications to the Taipo layout are:

* M and W switched. I don't like the spread with pinky up, and M is more common than W.
* Period moved to an unshifted position, it's too important to need a modifier.
* 4-finger space and backspace from Ardux added. This is mostly so I can
    let my thumb float or keep on typing if it gets out of position.
* Mapping to send correct keys when the connected PC is set to the dvorak layout.
    I use dvorak normally, the mapping doesn't work without this.
* Modifications to the behaviour of the thumb keys. I want to be able to hold down the modifier
    and then enter several chords before releasing it. This makes it impossible to hold space
    and backspace but they have alternate mappings so it's not a problem.

Since I have 42 keys available there's also a second layout with a regular base (dvorak/qwerty)
and some shifted layers to get numbers and special keys. This is roughly based on the 
[https://github.com/aroum/Watchman-layouts](Watchman) layout.


