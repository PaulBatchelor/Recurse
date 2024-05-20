#!/bin/sh
IMFLAGS="-auto-level -threshold 45% -monochrome -resize 40% -posterize 2"

crushit()
{
    IN=$1
    pngcrush $IN
    mv pngout.png $IN
}

rotcc ()
{
    IN=$1
    OUT=$2

    convert $IN -rotate -90 $IMFLAGS $OUT
    crushit $OUT
}

rot ()
{
    IN=$1
    OUT=$2

    convert $IN -rotate 90 $IMFLAGS $OUT
    crushit $OUT
}

if  [ "$#" -lt 3 ]
then
    echo "Usage: $0 [rot|rotcc] in.jpg out.png"
    exit
fi

ORIENTATION=$1
IN=$2
OUT=$3

if [ "$ORIENTATION" == "rot" ]
then
    rot $IN $OUT
elif [ "$ORIENTATION" == "rotcc" ]
then
    rotcc $IN $OUT
else
    echo "Invalid rotation: $ORIENTATION"
fi
