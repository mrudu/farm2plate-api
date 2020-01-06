from skimage import io,color
import numpy as np
import sys
import math
ros_path = '/opt/ros/kinetic/lib/python2.7/dist-packages'
if ros_path in sys.path:
    sys.path.remove()
import cv2
sys.path.append('/opt/ros/kinetic/lib/python2.7/dist-packages')


# takes in image and list of verticies of the polygon(i.e. the mango's edges) 
# and fills the polygon white with black background after which a bitwise and
# is done with the original image to get mango with black background
def region_of_interest(img, vertices):
    width = img.shape[0]
    height = img.shape[1]
    mask = np.zeros_like(img)
    channel_count = img.shape[2]
    match_mask_color = (255,) * channel_count
    cv2.fillPoly(mask, vertices, match_mask_color)
    mask_gray = cv2.cvtColor(mask, cv2.COLOR_RGB2GRAY)
    count = 0 
    for x in range(width):
        for y in range(height):
            if mask_gray[x][y] == 255 :
                count += 1
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image, count




# uses edge detection and gets the outline of the mango and returns a list 
# of all the vertices of the mango's edge
def vertices(img, max):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(img,(5,5),100)
    canny = cv2.Canny(blur,80,80)
    width = img.shape[0]
    height = img.shape[1]
    list_vertices = []
    for x in range(0,width,max):
        for y in range(0,height,max):
            if canny[x][y] > 0:
                list_vertices.append((y,x))
    return list_vertices


# Takes in the image which has already been converted from rgb to lab and
# takes the mean value of each pixel in the picture
def mean_lab(img):
    width = img.shape[0]
    height = img.shape[1]
    L = 0
    a = 0
    b = 0
    count = 0
    for x in range(0,width,1):
        for y in range(0,height,1):
            if img[x][y][0] != 0 or img[x][y][1] != 0 or img[x][y][2] != 0:
                L += img[x][y][0]
                a += img[x][y][1]
                b += img[x][y][2]
                count += 1
    L /= count
    a /= count
    b /= count
    a += 9
    return [L,a,b]



# finds number of spots in the image's mango (count)
def spots(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)[1]
    width = img.shape[0]
    height = img.shape[1]
    count = 0
    for x in range(width):
        for y in range(height):
            if thresh[x][y] != 255 :
                count += 1
    return thresh, count



# find length of major and minor axis of mango
def major_and_minor(img, list_vertices):
    major1 = ()
    major2 = ()
    major_length = 0
    count = 0
    lengths = []
    for v1 in list_vertices[::5]:
        count += 5
        for v2 in list_vertices[count::5]:
            length = math.sqrt((v1[0] - v2[0])**2 + (v1[1] - v2[1])**2)
            if v1[0] == v2[0]:
                angle = math.pi / 2
            else:
                slope = (v2[1] - v1[1])/(v2[0] - v1[0])
                angle = math.atan(slope)
            len = {'length' : length, 'v1' : v1, 'v2' : v2, 'angle' : angle}
            lengths.append(len)
            if(len['length'] > major_length):
                major_length = len['length']
                major1 = tuple(len['v1'])
                major2 = tuple(len['v2'])

    center = [0,0]
    center[0] = (major1[0] + major2[0])/2
    center[1] = (major1[1] + major2[1])/2
    cv2.line(img,major1,major2,(255,0,0),5)

    if(major1[0] == major2[0]):
        angle = 0
    else:
        slope = (major2[1] - major1[1])/(major2[0] - major1[0])
        slope = -1/slope
        angle = math.atan(slope)
    minor1 = (0,0)
    minor2 = (511,511)
    minor_length = 0
    for len in lengths:
        if len['v1'][0] == len['v2'][0] :
            continue
        slope = (len['v2'][1] - len['v1'][1])/(len['v2'][0] - len['v1'][0])
        dist = ((center[1] - len['v1'][1]) - slope * (center[0] - len['v1'][0]))/math.sqrt(1 + slope**2)
        if(dist < 1):
            if abs(len['angle'] - angle) < math.pi/30 :
                if(len['length'] > minor_length):
                    minor_length = len['length']
                    minor1 = tuple(len['v1'])
                    minor2 = tuple(len['v2'])


    cv2.line(img,minor1,minor2,(255,0,0),5)
    ratio = major_length/minor_length
    return img, ratio, minor_length, major_length

def process_cie_lab(img_name):
    img_original = io.imread("uploads/"+img_name)
    ratio = img_original.shape[0]/img_original.shape[1]
    img = cv2.resize(img_original, (256,int(256*ratio)))
    list_vertices = vertices(img, 1)
    cropped_image, count_mango = region_of_interest(img, np.array([list_vertices], np.int32))
    lab = color.rgb2lab(cropped_image)
    lab_values = mean_lab(lab)
    blur = cv2.GaussianBlur(img,(5,5),0)
    canny = cv2.Canny(blur,30,30)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    image_with_axis, ratio, minor_length, major_length = major_and_minor(canny, list_vertices)
    spot_img, count_spots = spots(img_original)
    ratio_spots = count_spots/count_mango

    cie_lab_data = {}
    cie_lab_data["type"] = "FULL"
    cie_lab_data["fruit_id"] = img_name
    cie_lab_data["L_value"] = lab_values[0]
    cie_lab_data["a_value"] = lab_values[1]
    cie_lab_data["b_value"] = lab_values[2]
    cie_lab_data["minor_axis"] = minor_length
    cie_lab_data["major_axis"] = major_length
    cie_lab_data["count_spots"] = str(count_spots)
    cie_lab_data["count_mango"] = str(count_mango)
    cie_lab_data["ratio"] = str(ratio)
    cie_lab_data["ratio_spots"] = str(ratio_spots)
    
    return cie_lab_data
    
