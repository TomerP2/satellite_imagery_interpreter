import os
import pytest
from PIL import Image, ImageChops
from src.satellite_imagery_interpreter.core.process_rectangle import rectangle_to_aerial

def test_process_rectangle(tmp_path):
    # Define test inputs
    wgs84_coors = [(5.681000, 51.968959), (5.680468, 51.968872)]
    zoom_level = 17
    output_folder = tmp_path / "output"
    output_folder.mkdir()

    # Run the function
    tif_path, image = rectangle_to_aerial(wgs84_coors, zoom_level, str(output_folder))

    # Check if the output .tif file exists
    assert os.path.exists(tif_path), f"Output file {tif_path} does not exist."

    # Check if the returned image is a PIL Image object
    assert isinstance(image, Image.Image), "Returned object is not a PIL Image."

    # Check properties of the image (e.g., size)
    assert image.size[0] > 0 and image.size[1] > 0, "Image size is invalid."
    
    # Check if the image matches the expected .tif file
    expected_image = Image.open('./tests/assets/aerial.tif')
    diff = ImageChops.difference(image, expected_image)
    assert not diff.getbbox(), "The image object does not match the expected .tif file."

