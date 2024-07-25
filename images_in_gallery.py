# Copyright (c) 2024 hedane (https://github.com/hedane)

from invokeai.invocation_api import (
    BaseInvocation,
    WithBoard,
    ImageField,
    InvocationContext,
    invocation,
    ImageCollectionOutput,
)


@invocation("images_in_gallery", title="Images In Gallery", tags=["primitives", "image", "collection", "gallery"], category="primitives", version="1.0.0", use_cache=False)
class ImagesInGalleryInvocation(BaseInvocation, WithBoard):
    """Collects all images on selected board in gallery"""

    def invoke(self, context: InvocationContext) -> ImageCollectionOutput:
        board_id = self.board.board_id if self.board else "none"
        image_names = context.boards.get_all_image_names_for_board(board_id)
        # context.logger.debug(str([board.board_id for board in context.boards.get_all()]))
        collection: list[ImageField] = [ImageField(image_name=image_name) for image_name in image_names]
        return ImageCollectionOutput(collection=collection)
