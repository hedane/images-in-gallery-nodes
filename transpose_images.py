# Copyright (c) 2024 hedane (https://github.com/hedane)

from invokeai.invocation_api import (
    BaseInvocation,
    ImageField,
    InputField,
    InvocationContext,
    invocation,
    ImageCollectionOutput,
)


@invocation("transpose_images", title="Transpose Images", tags=["image", "collection"], category="collections", version="1.0.0", use_cache=False)
class TransposeImagesInvocation(BaseInvocation):
    """Transpose images, e.g. 3x2: [1,2,3,4,5,6] to [1,4,2,5,3,6]"""

    collection: list[ImageField] = InputField(description="The collection of image values")
    size: int = InputField(ge=1, description="Size of images(2 of 3x2)", default=2)

    def invoke(self, context: InvocationContext) -> ImageCollectionOutput:
        collection: list[ImageField] = []
        length = len(self.collection)
        base = length // self.size
        for i in range(base):
            for j in range(i, length, base):
                collection.append(self.collection[j])
        return ImageCollectionOutput(collection=collection)
