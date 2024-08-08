# Copyright (c) 2024 hedane (https://github.com/hedane)

from PIL import ImageOps

from invokeai.invocation_api import (
    BaseInvocation,
    ImageField,
    InputField,
    InvocationContext,
    invocation,
    ImageOutput,
)


@invocation(
    "mask_invert",
    title="Mask Invert",
    tags=["image", "inpaint"],
    category="inpaint",
    version="1.0.0",
)
class MaskInvertInvocation(BaseInvocation):
    """Invert the image mask"""

    image: ImageField = InputField(description="The mask image to process")

    def invoke(self, context: InvocationContext) -> ImageOutput:
        mask = context.images.get_pil(self.image.image_name)

        mask_inverted = ImageOps.invert(mask.convert("L"))

        mask_dto = context.images.save(image=mask_inverted)

        return ImageOutput(
            image=ImageField(image_name=mask_dto.image_name),
            width=mask_dto.width,
            height=mask_dto.height,
        )
