import os
import shutil
from project import getFaces, getImg, askForName
import numpy as np

def test_getFaces():
    imagePath = "celebs/celeb (13).jpg"
    names, image = getFaces(imagePath) 
    assert names == []
    assert image is None
    
    imagePath = "celebs/celeb (1).jpg"
    names, image = getFaces(imagePath)
    assert len(names) > 0
    assert image is not None

def test_getImg():
    imagePath = "celebs/celeb (1).jpg"
    outputDir = "output"
    if os.path.exists(outputDir):
        shutil.rmtree(outputDir)
    os.makedirs(outputDir)
    getImg(imagePath, outputDir)
    assert len(os.listdir(outputDir)) > 0

def test_askForName():    
    faceImage = np.zeros((0, 0, 3), dtype=np.uint8)
    assert askForName(faceImage) == None