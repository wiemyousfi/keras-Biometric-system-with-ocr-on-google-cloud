
import matplotlib.pyplot as plt
from skimage.io import imsave
from skimage import measure, morphology
from skimage.transform import resize
from skimage.color import label2rgb
from skimage.measure import regionprops
import numpy as np
from PIL import Image
import cv2
#unifing size function
def resizing(img):
  img3 = Image.open(img)
  new_width  = 945
  new_height = 359
  img4 = img3.resize((new_width, new_height), Image.ANTIALIAS)
  return(img4)
  # Define box inside image

def cropping(image, left,top,width,height):
# Create Box
   box = (left, top, left+width, top+height)

    # Crop Image

   area = image.crop(box)
   area.save("signat.png")
   cropped= "signat.png"
   return(cropped)

   


def extracting(img):
  
# the parameters are used to remove small size connected pixels outliar 
  constant_parameter_1 = 84
  constant_parameter_2 = 250
  constant_parameter_3 = 100

# the parameter is used to remove big size connected pixels outliar
  constant_parameter_4 = 18

# read the input image
  #img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1]  # ensure binary

# connected component analysis by scikit-learn framework
  blobs = img > img.mean()
  blobs_labels = measure.label(blobs, background=1)
  image_label_overlay = label2rgb(blobs_labels, image=img, bg_label= 0. )

  fig, ax = plt.subplots(figsize=(10, 6))
  the_biggest_component = 0
  total_area = 0
  counter = 0
  average = 0.0
  for region in regionprops(blobs_labels):
      if (region.area > 10):
          total_area = total_area + region.area
          counter = counter + 1
    # print region.area # (for debugging)
    # take regions with large enough areas
      if (region.area >= 250):
          if (region.area > the_biggest_component):
              the_biggest_component = region.area

  average = (total_area/counter)


# experimental-based ratio calculation, modify it for your cases
# a4_small_size_outliar_constant is used as a threshold value to remove connected outliar connected pixels
# are smaller than a4_small_size_outliar_constant for A4 size scanned documents
  a4_small_size_outliar_constant = ((average/constant_parameter_1)*constant_parameter_2)+constant_parameter_3

# experimental-based ratio calculation, modify it for your cases
# a4_big_size_outliar_constant is used as a threshold value to remove outliar connected pixels
# are bigger than a4_big_size_outliar_constant for A4 size scanned documents
  a4_big_size_outliar_constant = a4_small_size_outliar_constant*constant_parameter_4

# remove the connected pixels are smaller than a4_small_size_outliar_constant
  pre_version = morphology.remove_small_objects(blobs_labels, a4_small_size_outliar_constant)
# remove the connected pixels are bigger than threshold a4_big_size_outliar_constant 
# to get rid of undesired connected pixels such as table headers and etc.
  component_sizes = np.bincount(pre_version.ravel())
  too_small = component_sizes > (a4_big_size_outliar_constant)
  too_small_mask = too_small[pre_version]
  pre_version[too_small_mask] = 0
# save the the pre-version which is the image is labelled with colors
# as considering connected components
  plt.imsave('pre_version4.png', pre_version)

# read the pre-version
  img = cv2.imread('pre_version4.png',0)
# ensure binary
  img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
# save the the result
  cv2.imwrite("output4.png", img)
  x= cv2.imread("output4.png")
  return x

#signature
resized=resizing("IMG.jpg")
resized1=resizing("Cheque.PNG")
area1= cropping(resized1, 520, 190, 370, 100)
image= cv2.imread(area1,0)
signature=extracting(image)
cv2.imwrite("Test/signature/sign.png", signature)
#date
area2= cropping(resized, 700, 175, 240 ,60)
image= cv2.imread(area2)
cv2.imwrite("date.png", image)
#montant chiffres
area3= cropping(resized, 700, 90, 220, 70)
image= cv2.imread(area3)
cv2.imwrite("chiffres.png", image)

#montant lettres
area4= cropping(resized, 250, 70, 500, 50)
image= cv2.imread(area4)
cv2.imwrite("lettres.png", image)