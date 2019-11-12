# GEP Text Extractor
Extract and parse latitude and longitude from screenshots of GEP, using OpenCV and Python.


## Steps of process:
1. Use Python algorithms to crop an image just when the text starts to appear. Compare the I and II images.

  **Original**
  ![Portal Home Page](https://github.com/alpha74/gep_text_extractor/blob/master/images/s1.png)

  **Cropped**:
  ![Portal Home Page](https://github.com/alpha74/gep_text_extractor/blob/master/images/s2.png)

2. Apply `PyTesseract` OCR to get the text in the image.
