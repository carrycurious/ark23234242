import cv2 as cv
import numpy as np

# Load the stereo images (left and right)
img_left = cv.imread(r'C:\Users\sandeep\Downloads\left.png', cv.IMREAD_GRAYSCALE)
img_right = cv.imread(r'C:\Users\sandeep\Downloads\right.png', cv.IMREAD_GRAYSCALE)

# Check if the images are loaded correctly
if img_left is None or img_right is None:
    print("Error loading images!")
    exit()

# Step 1: StereoSGBM Parameters (Stereo Semi Global Block Matching)
min_disp = 0   # Minimum disparity
num_disp = 16  # Number of disparities (maximum disparity - minimum disparity)
block_size = 5 # Block size for matching (higher values lead to less noise but slower processing)

# Initialize StereoSGBM object
stereo_sgbm = cv.StereoSGBM_create(
    minDisparity=min_disp,
    numDisparities=num_disp,
    blockSize=block_size,
    P1=8 * 3 * block_size ** 2,  # Tunable parameter
    P2=32 * 3 * block_size ** 2,  # Tunable parameter
    disp12MaxDiff=1,  # Maximum allowed difference for right-left disparity check
    uniquenessRatio=15,  # Threshold to eliminate bad matches
    speckleWindowSize=50,  # Speckle filtering (small noise removal)
    speckleRange=2,  # Maximum disparity variation within a window
)

# Step 2: Compute the disparity map
disparity = stereo_sgbm.compute(img_left, img_right).astype(np.float32) / 16.0
print(np.max(disparity))
print(np.min(disparity))

# Step 3: Normalize the disparity map for visualization
# Convert disparity to uint8 in the range [0, 255]
disparity_normalized = cv.normalize(disparity, None, 0, 255, cv.NORM_MINMAX)
disparity_normalized = np.uint8(disparity_normalized)

# Step 4: Invert the depth map (since the larger disparity represents farther points)
disparity_inverted = 255 - disparity_normalized

# Step 5: Apply a color map (red for closer, blue for farther)
colored_depth = cv.applyColorMap(disparity_inverted, cv.COLORMAP_JET)

# Step 6: Display the results
cv.imshow("Depth Map (Red for closer, Blue for farther)", colored_depth)
cv.waitKey(0)
cv.destroyAllWindows()
