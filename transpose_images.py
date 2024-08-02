# Copyright (c) 2024 hedane (https://github.com/hedane)

from invokeai.invocation_api import (
    BaseInvocation,
    ImageField,
    InputField,
    InvocationContext,
    invocation,
    ImageCollectionOutput,
)


@invocation(
    "transpose_images",
    title="Transpose Images",
    tags=["image", "collection"],
    category="collections",
    version="1.0.0",
    use_cache=False,
)
class TransposeImagesInvocation(BaseInvocation):
    """Transpose images, e.g. 3x2: [1,2,3,4,5,6] to [1,4,2,5,3,6]"""

    collection: list[ImageField] = InputField(
        description="The collection of image values"
    )
    batches: int = InputField(
        ge=1, description="Batches of images(N of MxN)", default=2
    )

    def invoke(self, context: InvocationContext) -> ImageCollectionOutput:
        collection: list[ImageField] = []
        length = len(self.collection)
        size = length // self.batches
        for i in range(size):
            for j in range(i, length, size):
                collection.append(self.collection[j])
        return ImageCollectionOutput(collection=collection)
