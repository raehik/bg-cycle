#!/usr/bin/env python3
#
# Cycle backgrounds for applications.
#

import os, random, glob, shutil, subprocess

#bg_dir = os.path.expanduser("~") + "/.backgrounds/"
bg_dir = "/home/raehik/.backgrounds/"
image_dir = "orig/"
exts = ["png", "jpg"]

def convert_image(infile, w, h, png = False):
    base, ext = os.path.splitext(infile)
    if png is True:
        ext = ".png"
    outfile = bg_dir + "bg/" + os.path.basename(base) + "_bg" + ext
    print(outfile)
    proc = subprocess.Popen([bg_dir + "convert-to-bg", "-w", w, "-v", h, infile, outfile])
    out, err = proc.communicate()
    return outfile

symlinks = [
        ["desktop", ""],
        ["grub", "/boot/grub/background-image.png"]
        ]
symlinks = [ [bg_dir + f, dest] for f, dest in symlinks ]

# get all background images available
images = []
for ext in exts:
    images.extend(glob.glob(bg_dir + image_dir + "*." + ext))

for f, dest in symlinks:
    # remove file if already present
    try:
        os.remove(f)
    except FileNotFoundError:
        pass

    # get a random image
    img = random.choice(images)

    print(f)
    if os.path.basename(f) == "grub":
        new_img = convert_image(img, "1366", "768", True)
    else:
        new_img = convert_image(img, "0", "0")

    # make symlinks
    os.symlink(new_img, f)

    # copy symlinked files (being pointing at) to elsewhere if required
    # (e.g. /boot/grub/)
    if dest == "":
        continue
    else:
        shutil.copy(f, dest)
