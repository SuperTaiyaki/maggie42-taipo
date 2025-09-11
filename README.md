This the customized firmware for my keyboard.
The concept was a keyboard primarily for typing on the [Taipo]() 10-key layout, hence the 8 yellow keys. 
It's entirely usable with only the left or right half connected, with a full-layout mode for both halves.

(TODO: photo)

The board is a Studio Purring (Tamaroh) [Maggie42cs0](https://github.com/tamaroh/maggie42cs0), built from one of their commercial PCBs.
As per the design it's running on a pair of RP2040-zeros.
Because this board is meant for chording the main switches are light Kailh Sakers. I should probably
have gone even lighter.

Base firmware is KMK as of late August 2025; I don't see anything resembling a version number.

Taipo firmware is based on [dlip's package](https://github.com/dlip/chouchou/tree/main/firmware/kmk).
The version in that source tree is outdated and doesn't quite work with current KMK.

Modifications to the Taipo layout are:

* All diagonals removed from the layout. I found them uncomfortable; they've been replaced
    with 3-finger chords.
* Period moved to an unshifted position, it's too important to need a modifier.
* 4-finger space and backspace from Ardux added. This is mostly so I can
    let my thumb float or keep on typing if it gets out of position.
* Mapping to send correct keys when the connected PC is set to the dvorak layout.
    I use dvorak normally, the mapping doesn't work without this.

On top of this the chording behaviour was changed slightly. With the original implementation by dlip
releasing a key would mark all the keys unpressed, and to use them in a combo they would have to be
released and pressed again. With this modified implementation releasing a key triggers the combo
(keypress), but pressing another key continues the combo and releasing a key will trigger
another keypress. So, to type the 'ppy' of 'sloppy':

* Press S and N (output a P)
* release N and press N again (output the 2nd P)
* release N and press I (output the Y)
* Release all keys

This also allows holding down thumb modifiers to type number sequences or in all-caps.

Since I have 42 keys available there's also a second layout with a regular base (dvorak/qwerty)
and some shifted layers to get numbers and special keys. This is roughly based on the 
[Watchman](https://github.com/aroum/Watchman-layouts) layout (and doesn't quite work yet).

