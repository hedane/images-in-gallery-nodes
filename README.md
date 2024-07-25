# images-in-gallery-nodes

An InvokeAI node for collecting all images on selected board in the gallery.

When I was using the InvokeAI workflow, I found that there was not a node to read images from the gallery, so I wrote one. I suggest that the official team could consider building this feature into the InvokeAI.

Usage: <Images In Gallery> -> <Iterate> -> image

Note: Due to a current API problem (bug?), it is not possible to read uncategorized board(board_id="none") in the gallery. Therefore, before using it, you need to manually move the images to a new board.

Additionally, after processing a batch of images [A0, B0, C0] n times, the output order is [A1, B1, C1, A2, B2, C2, ... An, Bn, Cn], which makes it difficult to compare and select. I also wrote a simple node to transpose the positions of the images, which can gather the scattered image order together, turning it into [A1, A2, ... An, B1, B2, ... Bn, ...].

Usage: <Images In Gallery> -> <Transpose Images> -> <Iterate> -> <Save Image>

My English is not good, this sentence was translated by AI :-)
