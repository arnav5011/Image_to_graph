import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import comb

def bezier(t, points):
    """Compute a point in a Bezier curve given control points and parameter t."""
    n = len(points) - 1
    point = np.zeros(2)
    for i in range(n + 1):
        binomial_coeff = comb(n, i)
        point += binomial_coeff * ((1 - t) ** (n - i)) * (t ** i) * np.array(points[i])
    return point

def bezier_equation(points):
    """Generate Desmos-compatible Bezier curve equations. Ensure Desmos y-axis is inverted"""
    n = len(points) - 1
    x_terms = []
    y_terms = []
    
    for i in range(n + 1):
        binomial_coeff = comb(n, i)
        x_term = f'{binomial_coeff} * (1 - t)^{n - i} * t^{i} * {points[i][0]}'
        y_term = f'{binomial_coeff} * (1 - t)^{n - i} * t^{i} * {points[i][1]}'
        x_terms.append(x_term)
        y_terms.append(y_term)
    
    x_eq = ' + '.join(x_terms)
    y_eq = ' + '.join(y_terms)
    
    return x_eq, y_eq

def filter_points(points, min_dist=5):
    """Filter points that are too close to each other."""
    filtered_points = [points[0]]
    for point in points[1:]:
        if np.linalg.norm(point - filtered_points[-1]) >= min_dist:
            filtered_points.append(point)
    return filtered_points

def fit_bezier_curve(points, group_size=3):
    """Fit Bezier curves with smaller groups of points."""
    curves = []
    for i in range(0, len(points) - group_size + 1, group_size):
        curve_points = points[i:i + group_size + 1]
        curves.append(curve_points)
    return curves
with open("Bezier Equations.txt", 'w') as file:
    pass
#Load image- The less complex the image the better
image = cv2.imread('image.png', cv2.IMREAD_GRAYSCALE)

#Resize the image to reduce complexity
resized_image = cv2.resize(image, (800, 600)) #Feel free to change this based on requirements

#Apply Gaussian blur to reduce noise to get clearer image
blurred_image = cv2.GaussianBlur(resized_image, (5, 5), 0) #Feel Free to change this based on requirements

# Step 4: Perform Canny edge detection
edges = cv2.Canny(blurred_image, 1, 100)
"""Feel free to change the parameters for Canny function based on requirements and image properties. 
Increasing lower threshold or reducing upper threshold reduces edge details and vice-versa"""

# Display the edges for checking
plt.figure(figsize=(10, 6))
plt.imshow(edges, cmap='gray')
plt.title('Canny Edge Detection')
plt.savefig('Edges.png', format='png')
plt.show()

#Find contours
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#Simplify contours using approximation with a finer epsilon
epsilon_factor = 0.0005  # Lower value increases detailings, adjust as needed
approx_contours = [cv2.approxPolyDP(contour, epsilon_factor * cv2.arcLength(contour, True), True) for contour in contours]

#Display approximate contours
approx_contour_image = cv2.cvtColor(resized_image, cv2.COLOR_GRAY2BGR)
cv2.drawContours(approx_contour_image, approx_contours, -1, (255, 0, 0), 1)

plt.figure(figsize=(10, 6))
plt.imshow(approx_contour_image)
plt.title('Approximate Contours')
plt.savefig('Contours Used.png', format='png')
plt.show()

#Extract points from contours and filter them so with minimum distance
filtered_points_list = []
for contour in approx_contours:
    points = contour[:, 0, :]  # Extract points from contour
    filtered_points = filter_points(np.array(points), min_dist=1)# Increasing minimum distance, increases accuracy
    filtered_points_list.append(filtered_points)

#Fit Bezier curves to each contour segment
for filtered_points in filtered_points_list:
    curves = fit_bezier_curve(filtered_points, group_size=4)  # Adjust group_size for finer curves
    
    for curve in curves:
        x_eq, y_eq = bezier_equation(curve)
        with open('Bezier Equations.txt', 'a') as file:
            file.write(f'({x_eq}, -({y_eq}))\n')
        print(f'({x_eq}, -{y_eq})')

        # Plot the Bezier curve
        t_values = np.linspace(0, 1, 100)
        bezier_points = [bezier(t, curve) for t in t_values]
        bezier_points = np.array(bezier_points)
        plt.plot(bezier_points[:, 0], bezier_points[:, 1])

# Final plot adjustments
plt.gca().invert_yaxis()
plt.title('Bezier Curves Fitted to Approximate Contours')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.savefig('Plot.png', format='png')
plt.show()
