#!/bin/bash
mpy=../mpy-cross-linux-amd64-10.1.4.static

find kmk -name '*.py' | while read fn
do
    TARGET="kmk_mpy/${fn#kmk/}"
    TARGET="${TARGET%py}mpy"
    mkdir -p $(dirname "$TARGET")
    ${mpy} -o "${TARGET}" ${fn}
done

