from PIL import Image
import numpy as np
from pathlib import Path
import os

def create_tiles(aerial_img: Image, tile_size_m: float, overlap_m: float, zoom: int, OUTPUT_F: str) -> Path:
    """
    Splits input image up into tiles of certain size (in meters) and certain overlap (in meters).
    
    Tiles will have name: {xcoor}_{ycoor}.png. xcoor and ycoor are in respect to the input image.
    
    Args:
        aerial_img (PIL.Image): Satellite image of the area.
        tile_size_m (float): Height and width of a tile in meters.
        overlap_m (float): Overlap between tiles in meters.
        zoom (int): Chosen zoom level.
        OUTPUT_F (str): Output folder path.

    Returns:
        tiles_f: Path to tiles folder
    """

    tiles_f = Path(OUTPUT_F) / 'tiles'
    os.mkdir(tiles_f)
    
    aerial_np = np.array(aerial_img)

    aerial_width = int(aerial_np.shape[0])
    aerial_height = int(aerial_np.shape[1])

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
            tile = aerial_np[x:end_x, y:end_y]
            
            # Get tile image from np array and save
            im = Image.fromarray(tile)
            im.save(Path(tiles_f) / f"{x}_{y}.png")
        
    return tiles_f