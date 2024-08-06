# Copyright (c) 2024 hedane (https://github.com/hedane)

from invokeai.invocation_api import (
    BaseInvocation,
    ImageField,
    InputField,
    InvocationContext,
    invocation,
    MetadataField,
    MetadataOutput,
)


@invocation(
    "image_metadata",
    title="Image Metadata",
    tags=["image", "metadata"],
    category="primitives",
    version="1.0.0",
)
class ImageMetadataInvocation(BaseInvocation):
    """get metadata of image"""

    image: ImageField = InputField(description="The image to get metadata")

    def invoke(self, context: InvocationContext) -> MetadataOutput:
        metadata: MetadataField = context.images.get_metadata(self.image.image_name)
        if metadata is None:
            metadata = MetadataField.model_validate({})
        return MetadataOutput(metadata=metadata)
