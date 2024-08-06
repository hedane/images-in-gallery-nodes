# Copyright (c) 2024 hedane (https://github.com/hedane)

from PIL import Image
from typing import Tuple


def calc_min_mask_box(mask: Image) -> "Box":
    img = mask.convert("1")
    pixels = img.load()
    # init to max/min
    box = Box(img.width, img.height, 0, 0)
    for y in range(img.height):
        for x in range(img.width):
            if pixels[x, y] == 0:
                if box.left > x:
                    box.left = x
                if box.right < x:
                    box.right = x
                if box.top > y:
                    box.top = y
                if box.bottom < y:
                    box.bottom = y
    if box.left > box.right:
        box.left, box.right = box.right, box.left
    if box.top > box.bottom:
        box.top, box.bottom = box.bottom, box.top
    return box


class Box:
    left: int = 0
    top: int = 0
    right: int = 0
    bottom: int = 0

    def __init__(
        self, left: int = None, top: int = None, right: int = None, bottom: int = None
    ):
        if left:
            self.left = left
        if top:
            self.top = top
        if right:
            self.right = right
        if bottom:
            self.bottom = bottom

    def height(self) -> int:
        return self.bottom - self.top

    def width(self) -> int:
        return self.right - self.left

    def pos(self) -> Tuple[int, int]:
        return self.left, self.top

    def end_pos(self) -> Tuple[int, int]:
        return self.right, self.bottom

    def size(self) -> Tuple[int, int]:
        return self.width(), self.height()

    def tuple(self) -> Tuple[int, int, int, int]:
        return self.pos() + self.end_pos()

    def copy(self) -> "Box":
        return Box(*self.tuple())

    def pad(self, padding: int) -> "Box":
        return Box(
            self.left - padding,
            self.top - padding,
            self.right + padding,
            self.bottom + padding,
        )

    def offset(self, x: int = None, y: int = None) -> "Box":
        box = self.copy()
        if x:
            box.left += x
            box.right += x
        if y:
            box.top += y
            box.bottom += y
        return box

    def intersect(self, box: "Box") -> "Box":
        ibox = box.copy()
        if self.left > ibox.left:
            ibox.left = self.left
        if self.right < ibox.right:
            ibox.right = self.right
        if self.top > ibox.top:
            ibox.top = self.top
        if self.bottom < ibox.bottom:
            ibox.bottom = self.bottom
        return ibox
