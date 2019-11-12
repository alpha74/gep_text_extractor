"""
	Using OpenCV.
"""

import cv2
import numpy as np
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\INSTALLS\Tesseract-OCR\tesseract.exe'

"""
	Convert image data to complete black and white using certain algo.
	Returns new image object.
"""
def cvt_completebw( img, show_details = 1 ):
	img_shape = img.shape
	img_width = img_shape[1]
	img_height = img_shape[0]
	
	if( show_details == 1 ):
		print( "Image shape:" + str(img.shape) )
		print( "Height: " + str(img_height) + "  Width: " +str(img_width )) 
		print( "Image size: " + str(img.size ) )
	
	new_img = np.zeros( (img_height, img_width, 3 ), np.uint8 )
	
	# Good Parameters values. Can be changed for better results. BGR.
	LIMIT1 = 120
	LIMIT2 = 120
	LIMIT3 = 80
	
	
	for i in range (0,img_height):
		for j in range (0,img_width):
			if( img[i][j][0] > LIMIT1 and img[i][j][1] > LIMIT1 and img[i][j][2] > LIMIT1 ):
				new_img[i][j] = 255
				
	
	cv2.imshow( "BW", new_img )
	
	return new_img			
	

"""
	Returns rectangle coordinates.
"""

def get_text_rect( img, show_details = 1 ):
	
	scaleplus = 500
	width = int( img.shape[1] * scaleplus / 100 )
	height = int( img.shape[0] * scaleplus / 100 )
	dim = ( width, height )

	# Resize image. Enlarge image.
	img = cv2.resize( img, dim, interpolation = cv2.INTER_AREA )
	
	img_shape = img.shape
	img_width = img_shape[1]
	img_height = img_shape[0]
	
	# Convert imgae to gray
	gray = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY )
	(thresh, blackAndWhiteImage) = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
	
	# Convert to Canny Edges
	edges = cv2.Canny(img,300,400)	

	cv2.imshow( "Gray - canny", edges )		
	(thresh, blackAndWhiteImage) = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
	cv2.imshow( "Gray", blackAndWhiteImage )	
	
	# new_img = np.zeros( (img_height, img_width, 1 ), np.uint8 )
	
	# good_indices:  Indices (x,y) whose pixel value is above a limit
	top_left = [ 9999,9999 ]		# Belongs to good_indices. Indicates the min Top Left pixel.
	top_right = [ 0, 0 ]			# Belongs to good_indices. Indicates the top_right corner of text.
	
	
	# Image used:
	ext_img = gray
	# Finding top_left
	for x in range (4, int(img_width/4) ):		
		for y in range (4, int( img_height * 0.75 ) ):
		
			# Calculate difference between current and previous pixel value.
			val = int( ext_img[y][x] ) - int( ext_img[y][x-1] )
			val = abs( val )
			
			# Filter limit value.
			LIMIT = 50
			
			if( val > LIMIT ):
				#print( str( ext_img[i][j] ) + "-" + str( ext_img[i][j-1] ), end = "" )
				#print( "=" + str( val ) )
				
				# Rule
				if( x < top_left[0] ):
					top_left[0] = x 
				
				if( y < top_left[1] ):
					top_left[1] = y
			
	
	# Mark the hit point on temp image.
	temp_img = img
	cv2.circle(temp_img,(top_left[0], top_left[1]), 2, (0,255,0), -1)
	
	
	
	# Finding top_right
	for x in range ( int(img_width * 0.75) ,img_width ):		
		for y in range (1, int(img_height * 0.5 ) ):
		
			# Calculate difference between current and previous pixel value.
			val = int( ext_img[y][x] ) - int( ext_img[y][x-1] )
			val = abs( val )
			
			# Filter limit value.
			LIMIT = 50
			
			if( val > LIMIT ):											
				# Rule
				if( x > top_right[0] ): 
					top_right[0] = x
										
				
	# We already y-coordinate.
	top_right[1] = top_left[1]

	# Mark second hit point
	cv2.circle( temp_img, ( top_right[0],top_right[1]), 2, (255,0,0), -1 )
	cv2.imshow( "Hit Points", temp_img )
		
	print( "TL: " + str( top_left ) + "  TR: " + str( top_right ) )
	
	
	# Return Top left and Bottom Right pixel coordinates.
	return top_left, top_right


"""
	Runs OCR on image.
"""
def run_ocr( img ):
		
	scale = 20
	width = int( img.shape[1] * scale / 100 )
	height = int( img.shape[0] * scale / 100 )
	dim = ( width, height )

	# Resize image. Diminish image.
	img = cv2.resize( img, dim, interpolation = cv2.INTER_AREA )
	
	cv2.imshow( "sub size", img )
	cv2.imwrite( "sub-image.png", img )
	
	text = pytesseract.image_to_string( "sub-image.png", lang="eng",config = "--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789.-")
	
	return text


"""
	Reads image and displays rectangle over text.
"""
def show_rect( imgpath, imgname = "img" ):
	
	# Read the image from path.
	img = cv2.imread( imgpath )
	
	# Display original image.
	cv2.imshow( "Orig " + imgname, img )
	
	# Convert image to complete black and white.
	img_bw = cvt_completebw( img, 1 )

	# Get rectangle coordinates.
	tl, tr = get_text_rect( img_bw, 0 )
	
	
	# Resize image.
	scaleplus = 500
	width = int( img.shape[1] * scaleplus / 100 )
	height = int( img.shape[0] * scaleplus / 100 )
	dim = ( width, height )
	img = cv2.resize( img, dim, interpolation = cv2.INTER_AREA )

	# Using pixel height from GEP and displaying instead of actual returned value.
	gepw = 12 * 5

	
	# Do corrections on rectangle.
	tl[0] = tl[0]
	tl[1] = tl[1] - 5
	tr[0] = tr[0] + 5
	tr[1] = tr[1] + gepw + 5
	
	
	print( "Rectangle coordinates: " + str( tl ) + " " + str( tr ) )

	# Draw rectangle over image and display.
	rect_img = img
	cv2.rectangle( rect_img, ( tl[0], tl[1]), ( tr[0], tr[1] ) ,(0,255,0), 1 )	
	cv2.imshow( "Extraction " + imgname, rect_img )
	
	# Create new variables
	x1 = tl[0]
	y1 = tl[1]
	x2 = tr[0]
	y2 = tr[1]
	
	# Create sub-image from rectangle
	try:
		sub_img = img[ y1 : y2, x1 : x2 ]
		cv2.imshow( "Sub-image", sub_img )
		
		text = run_ocr( sub_img )
		print( "OCR: " + text )
	
	except Exception as e:
		print( "EXCEPTION: " + str(e) )
	
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	
	return 1


# ===============================================================


#show_rect( "s1.png", "s1" )

def run_all( i, j):
	
	while( i <= j ):
		
		filename = "s" + str(i) + ".png"
		
		print( "\n --Running file" + filename )
		show_rect( filename )
		
		i = i + 1
	
	print( "\n Completed." )
	

# ============================================================

run_all( 1, 9 )
	