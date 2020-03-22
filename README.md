# GEP Text Extractor
Extract and parse latitude and longitude from screenshots of GEP, using OpenCV and Python.


## Steps:
1. Take screenshot of specified coordinates on screen.
2. Use Python `OpenCV` image library to crop the image. 
3. Cropping requires some self made observations and alogorithms( Compare the __Original__ and __Cropped Images__ images ).
3. Apply `PyTesseract` OCR to get the text in the image.


## Demo Images: 

  **Original**
  ![Portal Home Page](https://github.com/alpha74/gep_text_extractor/blob/master/images/s1.png)

  **Cropped**:
  ![Portal Home Page](https://github.com/alpha74/gep_text_extractor/blob/master/images/s2.png)
  
  **OCR PyTesseract**
  Output: 74.241590
