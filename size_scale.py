# Copyright (c) 2024 hedane (https://github.com/hedane)

from invokeai.invocation_api import (
    BaseInvocation,
    BaseInvocationOutput,
    InvocationContext,
    invocation,
    invocation_output,
    InputField,
    OutputField,
)


@invocation_output("size_scale_output")
class SizeScaleOutput(BaseInvocationOutput):
    """Base class for SizeScale output"""

    width: int = OutputField(description="The scaled width of the image (in pixels)")
    height: int = OutputField(description="The scaled height of the image (in pixels)")


@invocation("size_scale", title="Size Scale", tags=["math"], version="1.0.0")
class SizeScaleInvocation(BaseInvocation):
    """Calculates the size with scale factor for image in 8 pixels"""

    width: int = InputField(ge=8, default=512, description="Source image width")
    height: int = InputField(ge=8, default=768, description="Source image height")
    scale_factor: float = InputField(
        gt=0.0001, default=1.0, description="Amount to scale size"
    )

    def invoke(self, context: InvocationContext) -> SizeScaleOutput:
        width = int(self.width * self.scale_factor)
        height = int(self.height * self.scale_factor)

        width = (width // 8) * 8
        height = (height // 8) * 8

        return SizeScaleOutput(width=width, height=height)
