from PIL import Image
import numpy as np
import os

def create_tiles(aerial_img, tile_size_m, overlap_m, zoom, OUTPUT_F):
    # IN: 
    # aerial_path: Path to .tif of satellite view of the area
    # tile_size_m: User input. Height/width of a tile in meters.
    # overlap_m: User input. Overlap between tiles in meters
    # zoom: User input. Chosen zoom level.

    tiles_f = os.path.join(OUTPUT_F, 'tiles')
    aerial = np.array(aerial_img)

    aerial_width = int(aerial.shape[0])
    aerial_height = int(aerial.shape[1])

    tiles = []
    idx_coors = {}
    
    # Convert inputs in meters to pixels
    m_per_pixel = (3440.640 / 2**zoom) # From https://www.geonovum.nl/uploads/standards/downloads/nederlandse_richtlijn_tiling_-_versie_1.1.pdf
    tile_size = int(tile_size_m / m_per_pixel)
    overlap = int(overlap_m / m_per_pixel)

    # Loop slices image into tiles with overlap
    for x in range(0, aerial_width - tile_size + overlap + 1, tile_size - overlap):
        for y in range(0, aerial_height - tile_size + overlap + 1, tile_size - overlap):
            # Calculate end indices ensuring not to exceed the image dimensions
            end_x = x + tile_size if (x + tile_size <= aerial_width) else aerial_width
            end_y = y + tile_size if (y + tile_size <= aerial_height) else aerial_height
            tile = aerial[x:end_x, y:end_y]
            tiles.append(tile)
            idx_coors[len(tiles)-1] = [y, x]  # Store the start coordinates of each tile
            
    # Save each tile as an image
    for i, tile in enumerate(tiles):
        im = Image.fromarray(tile)
        im.save(os.path.join(tiles_f,f"tile_{i}.png"))
    return idx_coors