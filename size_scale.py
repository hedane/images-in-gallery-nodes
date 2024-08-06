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

    width: int = OutputField(description="The scaled width (in pixels)")
    height: int = OutputField(description="The scaled height (in pixels)")
    scale_factor: float = OutputField(description="The scaled factor")


@invocation("size_scale", title="Size Scale", tags=["math"], version="1.0.0")
class SizeScaleInvocation(BaseInvocation):
    """Calculates the scaling size, ensuring to be multiple of 8 pixels"""

    width: int = InputField(ge=8, default=512, description="Source image width")
    height: int = InputField(ge=8, default=512, description="Source image height")
    scale_to: int = InputField(
        ge=128, default=768, description="Size of bigger side to scale"
    )

    def invoke(self, context: InvocationContext) -> SizeScaleOutput:
        scale_factor = self.scale_to / max(self.width, self.height)

        width = int(self.width * scale_factor)
        height = int(self.height * scale_factor)

        width = (width // 8) * 8
        height = (height // 8) * 8

        return SizeScaleOutput(width=width, height=height, scale_factor=scale_factor)
