
# README: Bezeir Curve Fitting and Desmos-Compatible Equation Generation
##  Introduction to Bezeir Curves
A **Bezeir curve** is a parametric curve that is widely used in computer graphics, vector design, and mathematical modeling. The curve is defined by a set of control points, and its shape is determined by these points. The curve's mathematical foundation is based on Bernstein polynomials and binomial coefficients. Bezeir curves are especially popular because they allow for smooth, scalable designs and are simple to compute using a recursive linear interpolation process.

In this code,  Bezeir curves are used to fit contours detected in an image after applying edge detection algorithms. The goal is to generate Desmos-compatible Bezeir curve equations based on the control points extracted from image contours.

## Requirements
The following libraries are required to run the code:
- OpenCV (cv2)
- NumPy
- Matplotlib
- SciPy

## Image Input

Input image should be named image.png.

The image will be resized to the dimensions defined by width and height.

The default size is set to 800x600 pixels, but you can modify these based on your requirements.

## Code Functionality

### Steps:

1. Load and Resize Image:

	The input image is loaded and resized to reduce complexity. This resizing helps with contour detection by reducing unnecessary details.

2. Gaussian Blurring:
	A Gaussian blur is applied to the image to reduce noise, making the edges clearer. The size of the blur kernel can be modified for better results.
Default kernel: (5, 5)

3. Canny Edge Detection:
	The code applies Canny edge detection to find the prominent edges in the image.Parameters for Canny Edge Detection:
	- Lower threshold: 1
	- Upper threshold: 100

**Important: These thresholds need to be adjusted depending on the image's contrast and complexity. Checking the output of the edge detection step is crucial to ensure proper contours are detected.**

4. Contour Detection and Approximation:
	Using the edges found by Canny, contours are extracted using the OpenCV function cv2.findContours. These contours are then approximated using a polygonal curve with the cv2.approxPolyDP function, which reduces unnecessary details while preserving the shape. The epsilon_factor determines the precision of this approximation: Default epsilon_factor: 0.0005

5. Filtering Points:
Points from the approximated contours are filtered based on a minimum distance (min_dist) to reduce noise and redundancy. Default min_dist: 1 pixel Increasing this value results in fewer points and a smoother curve.

6. Bezeir Curve Fitting:
The filtered contour points are divided into groups (defined by group_size), and Bezeir curves are fitted to each group. The binomial coefficients used in the Bezeir curve equation determine the influence of each control point.

7. Bezeir Equation Generation:
The code generates Desmos-compatible Bezeir curve equations for each segment. These equations are saved in a text file (Bezeir Equations.txt) in the following format: $x(t)$ and $y(t)$ equations are generated based on the control points. The equations are adjusted for Desmos. At the end of the file, additional boundary equations are provided for visualizing the image within the rectangular frame defined by (0, 0) and (width, -height).

8. Plotting Bezeir Curves:
Bezeir curves are plotted and displayed, with the y-axis inverted to match the coordinate system used by Desmos.


## Key Parameters

You can fine-tune these parameters to better suit your image:

1. width and height: Dimensions of the resized image. Higher values retain more details. Default is 800x600

2. Gaussian Blur Matrix: (5, 5) is the default. Increasing the matrix size will blur the image more, helping reduce noise.

3. Canny Edge Detection: These thresholds can be modified to include or exclude certain details.
	- Lower threshold: 1
	- Upper threshold: 100

4. min_dist: Minimum distance between consecutive points. Increasing this value leads to fewer control points, making the curve smoother.

5. group_size: Number of points in each Bezeir curve segment. Increasing this value gives more control points for each curve, leading to finer curves.

## Importance of Visualizing Results

It's essential to check the outputs of both the Canny edge detection and contour approximation steps before proceeding with curve fitting. If the edges or contours do not match the desired boundaries of the object, the Bezeir curves will not fit properly. Use the intermediate plots generated in the code (like Edges.png and Contours Used.png) to assess whether the detected edges and contours are correct.


## Desmos Plotting
The generated equations are saved in Bezeir Equations.txt. To visualize the fitted curves:

1. Copy all equations from the text file.
2. Paste them into Desmos's equation editor.
3. The image can be found in a rectangular frame defined by (0,0) and (width, -height). The inverted y-axis helps match the Desmos coordinate system.

A sample output is shown in Desmos_Output.png

## Outputs
1. Edges.png: Visualization of edges detected using the Canny algorithm.
2. Contours Used.png: Visualization of the simplified contours used for curve fitting.
3. Plot.png: Final plot with fitted Bezeir curves.

## Conclusion
This project helps in visualizing and generating smooth Bezeir curves from image contours. It outputs Desmos-compatible equations that can be used for further visualization and manipulation in the Desmos graphing calculator.