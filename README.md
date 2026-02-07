# AERIAL ROBOTICS KHARAGPUR (entry level tasks)

## SUBTASK1 (Construction of depth map by using 2 images)

### Abstract
This work addresses the problem of depth perception for a robot by generating a depth map from stereo images.

The implementation calculates depth by analyzing disparities between corresponding points in left and right camera images, effectively reconstructing the depth map and understanding the 3d environment for the robot luna.

Using the given images i computed the disparity matrix by matching the template on the same horizontal line. The featureful points in the matrix were saved and the depth was calculated using the relation (the depth is inversely proportion to the disparity).

Once the depth was calculated, the matrix was plotted using opencv to create a depth map which helps luna to visualize the 3d environment from the 2d images provided.

**FIELDS OF USE :**
- Autonomous Vehicles-to navigate through the 3d environement  
- 3D Modeling and Scanning:for generating 3d models from stereo images  

---

### I. INTRODUCTION

The problem is to help a robot named Luna, equipped with two parallel cameras, understand its surroundings. Luna is unsure whether to move forward due to objects in front of her.

The task is to develop a Python code that takes images from both cameras and generates a depth map visualizing the distance of objects, with closer objects appearing red and farther ones blue. breif it even smaller.

**Approach: The basic idea behind solving the problem was
to get the good points and calculate the disparity map.To do
the same i used the Shi thomasi and Harris algorithm built
into opencv to select the points.This attempt failed because
the number of points was extremely low and unable to plot
a dense depth with it. The next approach was computing the
disparity matrix and then clipping of the points with less
disparity as they tend to be flat regions . The problem is the
computation time is very high ( 30-40 seconds)**



---
### II.Problem statement

The task focuses on enabling a robot, Luna, to navigate its environment effectively. Luna, equipped with two cameras, struggles to process visual information for maneuvering, requiring a system to ”teach her to see.” Given stereo images from Luna’s cameras (”left.png” and ”right.png”), the
objective is to develop a Python code that generates a depth map, a visual representation of the environment’s depth. This depth map will use red for closer objects and blue for farther ones. The implementation should primarily involve creating the depth map generation from scratch, using basic library functions for support, by measuring the shift of elements
between the images. The final output includes the depth map (”depth.png”), code, and a detailed report.

---
### III. Final approach
## Approach

### 1) Libraries Used
- `numpy`
- `opencv`

Initially, the two given images are read, and a function for disparity is coded.

---

### 2) Disparity Computation
For computing the disparity matrix, a window of size **5** is taken for each pixel and matched with another window along the same horizontal axis.  
The shift in distance is then stored in the \((i, j)\)-th position of the disparity matrix.

---

### 3) Disparity Clipping
After computing the disparity matrix, points with extremely low disparity are clipped off, as these points tend to be flat or featureless.

The clipping range was chosen to be **(2–100)** after detailed analysis using percentiles and plotting the depth map multiple times.

---

### 4) Depth Computation
The depth is computed using the formula:

\[
Z = \frac{B \times f}{d}
\]

Where:
- **Z**: Depth of the point  
- **B**: Distance between cameras (baseline)  
- **f**: Camera focal length (in pixels)  
- **d**: Horizontal difference of corresponding points in the images (disparity)

However, only **relative depth** is required for computing the depth map. Hence, we assume:

\[
B = f = 1
\]

The depth values vary from **0–0.49**. The important observation is that the **93rd percentile lies at 0.16**, indicating that points above this threshold contribute little useful information.  
Therefore, clipping is performed at a suitable point:

```python
depth = np.clip(depth, 0, 0.14)



