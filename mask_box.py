# Copyright (c) 2024 hedane (https://github.com/hedane)

from PIL import Image
import random
from .common import Box, calc_min_mask_box

from invokeai.invocation_api import (
    BaseInvocation,
    ImageField,
    InputField,
    InvocationContext,
    invocation,
    invocation_output,
    ImageCategory,
    ImageOutput,
    OutputField,
)


@invocation_output("mask_box_output")
class MaskBoxOutput(ImageOutput):
    """Base class for MaskBox output"""

    mask: ImageField = OutputField(description="The output mask")
    x: int = OutputField(description="The x coordinate of the bounding box's left side")
    y: int = OutputField(description="The y coordinate of the bounding box's top side")


@invocation(
    "mask_box",
    title="Mask Box",
    tags=["image", "inpaint"],
    category="inpaint",
    version="1.0.0",
)
class MaskBoxInvocation(BaseInvocation):
    """Crop the images with smallest rect area on the mask"""

    image: ImageField = InputField(description="The image to process")

    mask: ImageField = InputField(description="The input mask to limit area")

    mask_x: int = InputField(
        default=0, description="Offset for the X-axis of the input mask"
    )
    mask_y: int = InputField(
        default=0, description="Offset for the Y-axis of the input mask"
    )

    padding: int = InputField(
        ge=0,
        default=50,
        description="All-axis padding around the output mask in pixels",
    )

    def invoke(self, context: InvocationContext) -> MaskBoxOutput:
        image = context.images.get_pil(self.image.image_name).convert("RGBA")
        mask = context.images.get_pil(self.mask.image_name).convert("L")

        # calc min mask box area
        box = calc_min_mask_box(mask)
        box = box.offset(self.mask_x, self.mask_y)

        image_box = Box(0, 0, image.width, image.height)
        result_box = box.pad(self.padding).intersect(image_box)

        # try pad the mask to image size
        if mask.size != image.size:
            mask2 = Image.new("L", image_box.size(), 255)
            mask2.paste(mask, box.pos())
        else:
            mask2 = mask

        result_image = image.crop(result_box.tuple())
        result_mask = mask2.crop(result_box.tuple())

        image_dto = context.images.save(image=result_image)
        mask_dto = context.images.save(
            image=result_mask, image_category=ImageCategory.MASK
        )

        return MaskBoxOutput(
            image=ImageField(image_name=image_dto.image_name),
            width=image_dto.width,
            height=image_dto.height,
            mask=ImageField(image_name=mask_dto.image_name),
            x=result_box.left,
            y=result_box.top,
        )
