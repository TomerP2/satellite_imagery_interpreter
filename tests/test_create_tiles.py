import pytest
from pathlib import Path
from PIL import Image
from src.satellite_imagery_interpreter.core.create_tiles import create_tiles

@pytest.fixture
def sample_image():
    """
    Create a PIL Image from .tif for testing.
    """
    tif_path = Path() / "tests" / "assets" / "aerial.tif"
    return Image.open(tif_path)

def test_create_tiles(sample_image, tmp_path):
    output_folder = tmp_path
    zoom = 17
    tile_size_m = 10
    overlap_m = 5

    result = create_tiles(
        aerial_img=sample_image,
        tile_size_m=tile_size_m,
        overlap_m=overlap_m,
        zoom=zoom,
        OUTPUT_F=str(output_folder),
    )

    tiles_dir = output_folder / "tiles"
    assert tiles_dir.exists(), "Tiles folder should be created"

    # Check that some tiles are written
    written_tiles = list(tiles_dir.glob("*_*.png"))
    assert len(written_tiles) > 0, "At least one tile should be written"

    # Check that first tile size is bigger than 0
    first_tile = Image.open(written_tiles[0])
    assert first_tile.size[0] > 0 and first_tile.size[1] > 0
