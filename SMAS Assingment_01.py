import numpy as np
import matplotlib.pyplot as plt
from skimage import data, transform
import imageio.v3 as iio

def transform_and_display(image, A, title):
    A_viz = A.astype(float).copy()
    
    # (b) Handle the singular matrix A5 by adding a tiny y-scale for visualization
    if np.linalg.det(A) == 0:
        A_viz[1, 1] = 0.01  
        
    h, w = image.shape[:2]
    cx, cy = w / 2, h / 2

    # 1. Translate image center to origin (0,0)
    T_center = np.array([
        [1, 0, -cx],
        [0, 1, -cy],
        [0, 0, 1]
    ])

    # 2. Flip the Y-axis so 'up' is positive, matching standard math coordinates
    T_flip = np.array([
        [1,  0, 0],
        [0, -1, 0],
        [0,  0, 1]
    ])

    # 3. Apply the 2x2 linear transformation matrix
    T_affine = np.eye(3)
    T_affine[:2, :2] = A_viz

    # Combine transforms (Forward mapping: Image -> Cartesian -> Transform -> Image)
    # T_center's inverse moves the origin back to the top-left corner
    M_forward = np.linalg.inv(T_center) @ T_flip @ T_affine @ T_flip @ T_center

    # Image warping requires the inverse mapping (Output pixels -> Input pixels)
    M_inverse = np.linalg.inv(M_forward)
    tform = transform.AffineTransform(matrix=M_inverse)

    # Warp the image (cval=1.0 fills out-of-bound areas with white)
    transformed_img = transform.warp(image, tform, output_shape=(h, w), cval=1.0)

    plt.figure(figsize=(5, 5))
    plt.imshow(transformed_img)
    plt.title(title)
    plt.axis('off')
    plt.show()

# Load your image here (e.g., image = iio.imread('your_image.jpg'))
# Using a standard sample image for demonstration:
image = data.astronaut()

# Define the matrices
matrices = {
    "A1 (Scaling)": np.array([[2, 0], [0, 0.5]]),
    "A2 (90° Rotation)": np.array([[0, -1], [1, 0]]),
    "A3 (Horizontal Shear)": np.array([[1, 1], [0, 1]]),
    "A4 (Y-axis Reflection)": np.array([[-1, 0], [0, 1]]),
    "A5 (X-axis Projection)": np.array([[1, 0], [0, 0]])
}

for title, A in matrices.items():
    transform_and_display(image, A, title)