# Internal modules
import math
import requests
import pprint
import math
import os
# External modules
import numpy as np
from pyproj import Transformer
import requests
from tqdm import tqdm
from PIL import Image

def rectangle_to_aerial(
    wgs84_coors: list[tuple[float, float]],
    zoom_level: int,
    output_folder: str,
    ) -> tuple[str, Image.Image]:
    """
    Parameters
    ----------
    wgs84_coors : list of tuple of float
        The corners of a rectangle in WGS-84 coordinates (longitude, latitude).
    zoom_level : int
        Zoom level, determines the quality/resolution of the aerial photo. #TODO Validate this is true. Remove parameter probably.
    output_folder : str
        Path to the output folder.

    Returns
    -------
    tif_path : str
        Path to the generated aerial photo (.tif) covering the rectangle area.
    image : PIL.Image.Image
        The combined aerial image as a PIL Image object.
    """
    # Create necessary folders
    for subfolder in ['pdok_data','tiles']:
        path = os.path.join(output_folder, subfolder)
        if not os.path.exists(path):
            os.makedirs(path)
    
    # Reproject coordinates from wgs84 to rd_new.
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:28992", always_xy=True)
    rd_new_coords = [transformer.transform(lon, lat) for lon, lat in wgs84_coors]

    # Extract x (easting) and y (northing) values
    x_coords = [coord[0] for coord in rd_new_coords]
    y_coords = [coord[1] for coord in rd_new_coords]

    # Compute rectangle bounds
    west_bound = math.floor(min(x_coords))
    east_bound = math.ceil(max(x_coords))
    south_bound = math.floor(min(y_coords))
    north_bound = math.ceil(max(y_coords))

    # Calculate tile length/width in meters based on chosen zoom level.
    # Values obtained from https://www.geonovum.nl/uploads/standards/downloads/nederlandse_richtlijn_tiling_-_versie_1.1.pdf
    meters_per_pixel = (3440.640 / 2**zoom_level)
    tile_length =  meters_per_pixel * 256

    # Create point grid across rectangle. One point per tile.
    x_points = np.arange(west_bound, east_bound + tile_length, tile_length)
    y_points = np.arange(north_bound, south_bound - tile_length, -tile_length)  # Start from y_max and go down
    grid = [[[float(x), float(y)] for x in x_points] for y in y_points]

    # Download the corresponding tile for each point in grid.
    tiles = {}
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            print (f'downloading tile {i*8 + j+1}/{len(grid) * len(grid[0])}')
            point = grid[i][j]
            path = download_tile(point[0],point[1],zoom_level, output_folder)
            tiles[(i,j)] = path

    # Combine tiles into one .tif
    tif_path = os.path.join(output_folder, "aerial.tif")
    image = combine_tiles_to_tif(tiles, tif_path)
    return tif_path, image
    
def download_tile(x, y, zoom, OUTPUT_F):
    # Van xy-coördinaten in RD naar XY-index van een tile bij zoomniveau Z 
    # (Bron: https://geoforum.nl/t/tile-column-en-tile-row-op-basis-van-coordinaten-x-y-z/8533/7)
    t = (903401.92-22598.08) * (0.5**zoom)  # 'tegelgrootte in meters'
    X = math.floor((285401.92+x)/t)  # 'rij-index van de tile'       
    Y = math.floor((903401.92-y)/t)  # 'kolomindex van de tile'
    tile=(X,Y)

    # Fetch tile from pdok WMTS-api
    url = f"https://service.pdok.nl/hwh/luchtfotorgb/wmts/v1_0/2023_orthoHR/EPSG:28992/{zoom}/{tile[0]}/{tile[1]}.jpeg"
    response = requests.get(url)

    if response.status_code == 200:
        path = os.path.join(OUTPUT_F, 'pdok_data', f'{x}_{y}.png')
        with open(path, 'wb') as f:
            f.write(response.content)
        return path
    else:
        print(response.status_code,response.text)


def combine_tiles_to_tif(tile_dict, output_path):
    """
    Combines multiple image tiles into a single TIFF image.
    Args:
        tile_dict (dict): A dictionary where keys are (row, col) tuples
            representing the grid position of each tile, and values are
            file paths to the corresponding image tiles.
        output_path (str): The file path where the combined TIFF image
            will be saved.
    Returns:
        PIL.Image.Image: The combined image as a PIL Image object.
    Notes:
        - Assumes each tile is 256x256 pixels and arranged in a regular grid.
        - The function pastes each tile into its correct position based on
          the (row, col) key.
        - The output image is saved in TIFF format.
    """

    tile_width = tile_height = 256
    
    # Extract the grid dimensions from the dictionary keys
    rows = max(key[0] for key in tile_dict.keys()) + 1
    cols = max(key[1] for key in tile_dict.keys()) + 1
    
    # Create an empty array to hold the combined image
    combined_width = cols * tile_width
    combined_height = rows * tile_height
    combined_image = Image.new("RGB", (combined_width, combined_height))
    
    # Paste each tile into the correct position
    for (row, col), tile_path in tile_dict.items():
        tile = Image.open(tile_path)
        x_offset = col * tile_width
        y_offset = row * tile_height
        combined_image.paste(tile, (x_offset, y_offset))
    
    # Save the combined image as a .tif file
    combined_image.save(output_path, format="TIFF")
    return combined_image
