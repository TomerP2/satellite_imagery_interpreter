from pathlib import Path
from ultralytics import YOLO

def detect_objects_in_images_folder(folder: Path, model_path: Path):
    """
    Uses a trained yolo_model to detect objects in images (.png) in a specified folder. 
    In:
        - folder: Path to a dictionary which contains the images.
        - model: Path to a trained yolo model.
        
    Out: An ultralytics Results object containing the results per image. See: https://docs.ultralytics.com/reference/engine/results/#ultralytics.engine.results.BaseTensor.to:~:text=ultralytics.engine.results.Results
    """
    model = YOLO(model_path)
    results = model(folder)
    return results


def detect_objects_in_tiles(tiles_folder: Path, model_path: Path):
    """
    Uses a trained yolo_model to detect objects in tiles (.png) in a specified folder. 
    
    **Expects the tiles to have the format {xcoor}_{ycoor}.png, with xcoor and ycoor being in reference to the full image**
    
    In:
        - tiles_folder: Path to a folder which contains the tiles.
        - model_path: Path to a trained yolo model.
        
    Out: 
    """
    