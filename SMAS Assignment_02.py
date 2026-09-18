import cv2
import numpy as np
import matplotlib.pyplot as plt
from google.colab import files
import ipywidgets as widgets
from IPython.display import display, clear_output

# 1. Upload the image
print("Please upload an image (JPG/PNG):")
uploaded = files.upload()

# 2. Load the image into memory
filename = next(iter(uploaded))
# Read image using OpenCV
img_bgr = cv2.imread(filename)

# Handle cases where image might have an alpha channel (PNG)
if img_bgr.shape[-1] == 4:
    img_bgr = cv2.cvtColor(img_bgr, cv2.COLOR_BGRA2BGR)

# Convert from BGR (OpenCV default) to RGB (Matplotlib/Standard)
original_image = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
current_image = original_image.copy()

print(f"Successfully loaded '{filename}'!")




# Create output area for the image
out_image = widgets.Output()

# Create UI Elements
action_dropdown = widgets.Dropdown(
    options=['Select Operation', 'Rotate', 'Resize', 'Flip', 'Shear', 'Custom Matrix', 'Reset'],
    value='Select Operation',
    description='Action:'
)

params_box = widgets.VBox() # Container for dynamic parameter inputs
apply_btn = widgets.Button(description="Apply Transformation", button_style='success')
apply_btn.layout.display = 'none' # Hide initially

# Dynamic Widgets for different operations
# Rotate
angle_slider = widgets.FloatSlider(value=90, min=-360, max=360, step=1, description='Angle:')

# Resize
fx_slider = widgets.FloatSlider(value=1.5, min=0.1, max=5.0, step=0.1, description='Scale X:')
fy_slider = widgets.FloatSlider(value=1.5, min=0.1, max=5.0, step=0.1, description='Scale Y:')

# Flip
flip_dir = widgets.Dropdown(options=['Horizontal', 'Vertical', 'Both'], description='Direction:')

# Shear
shear_x = widgets.FloatSlider(value=0.2, min=-2.0, max=2.0, step=0.1, description='Shear X:')
shear_y = widgets.FloatSlider(value=0.0, min=-2.0, max=2.0, step=0.1, description='Shear Y:')

# Custom Matrix
matrix_input = widgets.Text(
    value='1, 0.5, 0, 0, 1, 0', 
    description='[a,b,tx, c,d,ty]:', 
    style={'description_width': 'initial'},
    tooltip="Enter 6 numbers separated by commas for the 2x3 affine matrix"
)

# Function to draw the image
def show_image(img, title="Image"):
    with out_image:
        clear_output(wait=True)
        plt.figure(figsize=(6, 6))
        plt.imshow(img)
        plt.title(title)
        plt.axis('off')
        plt.show()



# Function to change parameters based on dropdown
def on_action_change(change):
    action = change['new']
    params_box.children = []
    apply_btn.layout.display = 'block'
    
    if action == 'Rotate':
        params_box.children = [angle_slider]
    elif action == 'Resize':
        params_box.children = [fx_slider, fy_slider]
    elif action == 'Flip':
        params_box.children = [flip_dir]
    elif action == 'Shear':
        params_box.children = [shear_x, shear_y]
    elif action == 'Custom Matrix':
        params_box.children = [matrix_input, widgets.HTML("<em>Format: top-left, top-right, x-shift, bottom-left, bottom-right, y-shift</em>")]
    elif action == 'Reset':
        apply_btn.description = "Reset to Original"
        params_box.children = []
    elif action == 'Select Operation':
        apply_btn.layout.display = 'none'
        
    if action != 'Reset':
        apply_btn.description = "Apply Transformation"

action_dropdown.observe(on_action_change, names='value')

# Function to apply the transformation
def apply_transformation(b):
    global current_image
    action = action_dropdown.value
    h, w = current_image.shape[:2]
    
    try:
        if action == 'Rotate':
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle_slider.value, 1.0)
            current_image = cv2.warpAffine(current_image, M, (w, h), borderValue=(255,255,255))
            
        elif action == 'Resize':
            current_image = cv2.resize(current_image, None, fx=fx_slider.value, fy=fy_slider.value)
            
        elif action == 'Flip':
            if flip_dir.value == 'Horizontal': code = 1
            elif flip_dir.value == 'Vertical': code = 0
            else: code = -1
            current_image = cv2.flip(current_image, code)
            
        elif action == 'Shear':
            M = np.float32([[1, shear_x.value, 0], [shear_y.value, 1, 0]])
            # Expand canvas slightly so sheared image isn't cut off
            new_w = int(w + abs(shear_x.value) * h)
            new_h = int(h + abs(shear_y.value) * w)
            current_image = cv2.warpAffine(current_image, M, (new_w, new_h), borderValue=(255,255,255))
            
        elif action == 'Custom Matrix':
            vals = [float(x.strip()) for x in matrix_input.value.split(',')]
            M = np.float32([[vals[0], vals[1], vals[2]], [vals[3], vals[4], vals[5]]])
            current_image = cv2.warpAffine(current_image, M, (w, h), borderValue=(255,255,255))
            
        elif action == 'Reset':
            current_image = original_image.copy()

        show_image(current_image, f"Result: {action}")
        
    except Exception as e:
        with out_image:
            clear_output(wait=True)
            print(f"Error applying transformation: {e}")

apply_btn.on_click(apply_transformation)

# Display the initial layout
ui = widgets.VBox([
    widgets.HTML("<h3>Interactive Image Transformation Toolbox</h3>"),
    action_dropdown, 
    params_box, 
    apply_btn
])

display(ui, out_image)
show_image(current_image, "Original Image")