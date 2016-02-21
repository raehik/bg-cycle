#!/usr/bin/env python3
#
# Cycle backgrounds for applications.
#

import sys
import os
import random
import glob
import shutil
import subprocess

#bg_dir = os.path.expanduser("~") + "/.backgrounds/"
bg_dir = "/home/raehik/.assets/backgrounds/"
image_dir = "orig/"
exts = ["png", "jpg"]

def convert_image(infile, w, h, png=False):
    base, ext = os.path.splitext(infile)
    if png is True:
        ext = ".png"
    outfile = bg_dir + "bg/" + os.path.basename(base) + "_bg" + ext
    print(outfile)
    proc = subprocess.Popen([bg_dir + "convert-to-bg", "-w", w, "-v", h, infile, outfile])
    out, err = proc.communicate()
    return outfile

def get_shuffled_images(argv):
    """Fills an array with all available images, shuffles it, then
    prepends any files given on as arguments."""
    LIST_START = 0
    images = []

    # get all backgrounds
    for ext in exts:
        images.extend(glob.glob(bg_dir + image_dir + "*." + ext))

    # random order
    random.shuffle(images)

    # insert any args at the start of the list (so they'll be picked
    # first)
    if len(argv) > 1:
        # reverse so that the first one is desktop, second is grub, etc.
        for img in reversed(argv[1:]):
            if img != "":
                img_path = bg_dir + image_dir + img
                images.insert(LIST_START, bg_dir + image_dir + img)
    return images

symlinks = [
        ["desktop", ""],
        ["grub", "/boot/grub/background-image.png"]
        ]
symlinks = [ [bg_dir + f, dest] for f, dest in symlinks ]

images = get_shuffled_images(sys.argv)

count = 0

for f, dest in symlinks:
    # remove file if already present
    try:
        os.remove(f)
    except FileNotFoundError:
        pass

    # get a random image
    img = images[count]

    if os.path.basename(f) == "grub":
        new_img = convert_image(img, "1366", "768", png=True)
    else:
        new_img = convert_image(img, "0", "0")

    # make symlinks
    os.symlink(new_img, f)

    # copy symlinked files (being pointing at) to elsewhere if required
    # (e.g. /boot/grub/)
    if dest != "":
        shutil.copy(f, dest)

    # increment counter
    count += 1
