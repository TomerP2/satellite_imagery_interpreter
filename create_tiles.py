from PIL import Image
import numpy as np
import os

def create_tiles(aerial_img, tile_size_m, overlap_m, zoom, downloads_f):
    # IN: 
    # aerial_path: Path to .tif of satellite view of the area
    # tile_size_m: User input. Height/width of a tile in meters.
    # overlap_m: User input. Overlap between tiles in meters
    # zoom: User input. Chosen zoom level.
    
    # 1. Gebruiker geeft tilesize in meters -> hoogte en breedte tile
    # 2. Gebruiker geeft tile overlap in meters -> overlap tussen tiles
    # 3. Gebruiker geeft zoomniveau -> Gebruik dit om m/pixel te bereken.
    # 4. Convert alle inputs van meters naar pixels adhv m/pixel.
    # 5. Bereken aantal tiles in width en height. Formule: aantal tiles = (aerial_width / tile_width) + (aerial_width / tile_width) * (overlap / tile_width)

    tiles = []
    idx_coors = {}
    m_per_pixel = (3440.640 / 2**zoom) # From https://www.geonovum.nl/uploads/standards/downloads/nederlandse_richtlijn_tiling_-_versie_1.1.pdf
    tile_size = tile_size_m / m_per_pixel
    overlap = overlap_m / m_per_pixel
    aerial = np.array(aerial_img)
    tiles_f = os.path.join(downloads_f, 'tiles')

    # Adjust the loop to slice tiles with overlap
    # Ensure loops do not create out-of-bound indices by adjusting the range limits
    for x in range(0, aerial.shape[0] - tile_size + overlap + 1, tile_size - overlap):
        for y in range(0, aerial.shape[1] - tile_size + overlap + 1, tile_size - overlap):
            # Calculate end indices ensuring not to exceed the image dimensions
            end_x = x + tile_size if (x + tile_size <= aerial.shape[0]) else aerial.shape[0]
            end_y = y + tile_size if (y + tile_size <= aerial.shape[1]) else aerial.shape[1]
            tile = aerial[x:end_x, y:end_y]
            tiles.append(tile)
            idx_coors[len(tiles)-1] = [y, x]  # Store the start coordinates of each tile
            
    # Save each tile as an image
    for i, tile in enumerate(tiles):
        im = Image.fromarray(tile)
        im.save(os.path.join(tiles_f,f"tile_{i}.png"))
    return idx_coors