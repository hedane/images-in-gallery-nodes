# Copyright (c) 2024 hedane (https://github.com/hedane)

from PIL import Image, ImageDraw, ImageFilter
from typing import Optional, Tuple
import random

from invokeai.invocation_api import (
    BaseInvocation,
    ColorField,
    ImageField,
    InputField,
    InvocationContext,
    invocation,
    invocation_output,
    ImageOutput,
    ImageCategory,
    OutputField,
)


@invocation_output("fill_shapes_output")
class FillShapesOutput(ImageOutput):
    """Base class for FillShapes output"""

    mask: ImageField = OutputField(description="The output mask")
    x: int = OutputField(description="The x coordinate of the bounding box's left side")
    y: int = OutputField(description="The y coordinate of the bounding box's top side")


@invocation(
    "fill_shapes",
    title="Fill Shapes",
    tags=["image", "inpaint"],
    category="inpaint",
    version="1.0.1",
    use_cache=False,
)
class FillShapesInvocation(BaseInvocation):
    """Fills solid shapes on image"""

    image: ImageField = InputField(description="The image to process")

    mask: Optional[ImageField] = InputField(
        default=None, description="The input mask to limit area"
    )
    mask_x: int = InputField(
        default=0, description="Offset for the X-axis of the input mask"
    )
    mask_y: int = InputField(
        default=0, description="Offset for the Y-axis of the input mask"
    )

    color: ColorField = InputField(
        default=ColorField(r=127, g=127, b=127, a=255),
        description="The color infill to shape",
    )

    num_shapes: int = InputField(default=3, description="Number of shapes")
    min_size: int = InputField(
        ge=3, default=5, description="Min size of shapes in pixels"
    )
    max_size: int = InputField(
        ge=5, default=20, description="Max size of shapes in pixels"
    )
    padding: int = InputField(
        ge=0,
        default=50,
        description="All-axis padding around the output mask in pixels",
    )

    _mask_edge_size: int = 0
    _mask_blur_radius: int = 4

    def invoke(self, context: InvocationContext) -> FillShapesOutput:
        image = context.images.get_pil(self.image.image_name).convert("RGBA")
        image_box = Box(0, 0, image.width, image.height)

        mask = None
        if self.mask:
            mask = context.images.get_pil(self.mask.image_name).convert("L")
            # calc min drawing box area
            draw_box = self.calc_min_mask_box(mask)
            draw_box_on_img = draw_box.offset(self.mask_x, self.mask_y)
        else:
            draw_box_on_img = draw_box = image_box

        image2 = image.crop(draw_box_on_img.tuple())
        image2_draw = ImageDraw.Draw(image2)
        mask2 = Image.new("L", draw_box.size(), 255)
        mask2_draw = ImageDraw.Draw(mask2)

        draw_size = draw_box.size()
        for _ in range(self.num_shapes):
            image2_draw, mask2_draw = self.draw_shape(
                image2_draw, mask2_draw, *draw_size
            )
        mask2 = mask2.filter(ImageFilter.BoxBlur(radius=self._mask_blur_radius))

        if mask:
            mask1 = mask.crop(draw_box.tuple())
            # invert cover by mask
            image2.paste(image.crop(draw_box_on_img.tuple()), mask=mask1)
            mask2.paste(Image.new("L", draw_box.size(), 255), mask=mask1)
            # paste to base image
            image3 = image  # more memory if use image.copy()
            image3.paste(image2, draw_box_on_img.pos(), image2)
            mask3 = Image.new("L", image_box.size(), 255)
            mask3.paste(mask2, draw_box_on_img.pos())
        else:
            image3 = Image.alpha_composite(image, image2)
            mask3 = mask2

        # use mask2 to reduce loop size
        result_box = (
            self.calc_min_mask_box(mask2)
            .offset(*draw_box_on_img.pos())
            .pad(self.padding)
            .intersect(image_box)
        )

        result_image = image3.crop(result_box.tuple())
        result_mask = mask3.crop(result_box.tuple())

        image_dto = context.images.save(image=result_image)
        mask_dto = context.images.save(
            image=result_mask, image_category=ImageCategory.MASK
        )

        return FillShapesOutput(
            image=ImageField(image_name=image_dto.image_name),
            width=image_dto.width,
            height=image_dto.height,
            mask=ImageField(image_name=mask_dto.image_name),
            x=result_box.left,
            y=result_box.top,
        )

    def draw_shape(
        self, draw: ImageDraw, mask_draw: ImageDraw, width: int, height: int
    ) -> Tuple[ImageDraw, ImageDraw]:
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        w = random.randint(self.min_size, self.max_size)
        h = random.randint(self.min_size, self.max_size)
        box = Box(x, y, x + w, y + h)

        draw.ellipse(box.tuple(), fill=self.color.tuple())
        mask_draw.ellipse(box.pad(self._mask_edge_size).tuple(), fill=0)
        return draw, mask_draw

    def calc_min_mask_box(self, mask: Image) -> "Box":
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
