import cv2 as cv
import numpy as np

img = cv.imread(r'C:\Users\sandeep\Downloads\left.png')
img2=cv.imread(r'C:\Users\sandeep\Downloads\right.png')
print(img.shape)
c = None  # Initialize variable

gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
gray_img2 = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)


d=0




def compute_disparity(left_image, right_image, x, y):
    global d 
   
    template_size=5
    
    half_t = template_size // 2

    # Extract template from the left image
    template = left_image[y - half_t : y + half_t + 1, x - half_t : x + half_t + 1]

    h, w = template.shape  
    img_h, img_w = right_image.shape

    min_ssd = float('inf')
    best_x = x  
    disparity = 0

   
    for shift in range(1,100):  
        if x - shift - half_t < 0:
            break  #
        

        patch = right_image[y - half_t : y + half_t + 1, x - shift - half_t : x - shift + half_t + 1]
        if(patch.shape!=template.shape):
            print(x,y)
        
        ssd = np.sum((patch - template) ** 2)  # Compute SSD

        if ssd < min_ssd:
            min_ssd = ssd
            best_x = x - shift
            disparity = shift  # Compute disparity
    if disparity>1:
        d=d+1
    return disparity

#the problem is that at 431,3 












disparity = np.zeros((381, 433), dtype=np.float32)
f=0
"""for corner in corners:
    x, y = corner.ravel()
    if x<430 and y<378: # Unpack the coordinates
        k=compute_disparity(gray_img,gray_img2,x,y)
        disparity[y,x]=k
        if k>1:
            f=f+1
print(f)"""

for y in range(1,378):
    for x in range(1,430):
        disparity[y][x]=compute_disparity(gray_img,gray_img2,x,y)
print(disparity.dtype)
print("Non-zero pixels after processing:", np.count_nonzero(disparity))

disparity_clipped = np.clip(disparity, 2, 100).astype(np.int32)

print("zero points", np.count_nonzero(disparity_clipped == 0))




print(f"Min: {np.min(disparity_clipped)}, Max: {np.max(disparity_clipped)}, 90th Percentile: {np.percentile(disparity_clipped, 90)}")



focal_length = 1 # Example focal length in pixels
baseline = 1  # Distance between cameras in meters


# Compute depth map using the formula
depth= (focal_length * baseline) / (disparity_clipped + 1e-6)  # Avoid division by zero
print(np.percentile(depth,4.5))
print(np.percentile(depth,20))
print(np.percentile(depth,40))
print(np.percentile(depth,60))
print(np.percentile(depth,80))
print(np.percentile(depth,90))
print(np.percentile(depth,91))
print(np.percentile(depth,92))
print(np.percentile(depth,93))
print(np.percentile(depth,94))
print(np.percentile(depth,95))
print(np.percentile(depth,98))






#low_disp_threshold = np.percentile(disparity, 4.5)  # Bottom 5% disparities


normalized_depth = np.zeros_like(depth, dtype=np.uint8)  # Initialize a blank image

# Normalize only the valid depth points
#mask = (depth >= mindep) & (depth <= maxdep)  # Mask for valid depth points


depth=np.clip(depth,0,0.18)
min=np.min(depth)
max=np.max(depth)





normalized_depth = ((depth - min) / (max - min) * 255).astype(np.uint8)

min=np.min(normalized_depth)
max=np.max(normalized_depth)
print("hi",min,max)




colored_depth = cv.applyColorMap(normalized_depth, cv.COLORMAP_JET)

kernel = np.ones((3,3), np.uint8)  # 3x3 kernel to make points bigger
dilated_depth = cv.dilate(colored_depth, kernel, iterations=1)
print(d)

cv.imshow("Depth Map", colored_depth)
cv.waitKey(0)
cv.destroyAllWindows()