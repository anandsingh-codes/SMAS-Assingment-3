# SMAS-Assingment-3


At the very top, the code imports four specialized toolkits. It brings in numpy to handle the heavy mathematical matrix calculations. It brings in matplotlib to actually draw and display the final pictures on your screen. It brings in skimage (Scikit-Image) which acts like a digital darkroom to handle the actual warping of the image pixels, and finally imageio to read image files from your computer.

The Core Function
The bulk of the code is a custom recipe, or function, called transform_and_display. You hand this recipe three things: an image, a 2-by-2 mathematical matrix (the rule for how to change the image), and a title for the final picture.

Preventing the Image from Disappearing
The very first thing the recipe does is check a mathematical property called the "determinant." In simple terms, it is checking if the math rule is going to completely flatten the image into a perfectly thin, invisible line (which happens with matrix A5). If it realizes the image is about to be completely crushed to zero thickness, it cheats just a little bit. It changes the zero to a tiny fraction (0.01). This doesn't change the math concept, but it leaves a tiny sliver of thickness so your human eyes can actually see the flattened image on the screen.

Finding the Middle
Next, it measures the height and width of the image to find the exact center point. This is important because, by default, computers think the coordinate (0,0) is at the very top-left corner of a picture. If you applied mathematical rotations to the top-left corner, the image would swing wildly off the screen. We want the image to spin and stretch around its own center.

Creating the "Sandwich" of Instructions
To make the math look right, the code has to perform a sequence of steps, like building a sandwich:

Move to Center: First, it creates a rule to slide the entire image so that its center point rests perfectly on the (0,0) origin of our imaginary graph.

Flip the Y-Axis: Second, it addresses a quirk of computers. On a computer screen, moving "down" means the Y-coordinates get bigger. In normal math, moving "up" means the Y-coordinates get bigger. The code creates a rule to flip the Y-axis upside down so that our standard math matrices behave exactly as we expect them to.

Apply your Math: Third, it takes your specific 2-by-2 matrix (like the 90-degree rotation or the reflection) and prepares to apply it.

Undo the Fixes: Finally, it creates rules to flip the Y-axis back to computer-mode, and slide the image back to its original corner so the computer can draw it properly.

Calculating the Reverse Path
The code combines all those steps into one master instruction called M_forward. However, it doesn't actually use this to draw the image. Instead, it calculates the exact opposite, called M_inverse.

This is a clever trick used in digital image processing. If you push original pixels forward to new locations, you often end up with empty holes or cracks in the final image because pixels might spread out. Instead, the computer looks at the final, blank canvas and goes pixel-by-pixel, asking the reverse question: "To color in this specific spot on the new canvas, which pixel do I need to go fetch from the original image?" This guarantees a smooth, solid picture without holes.

Painting the Final Picture
The transform.warp command is the moment the actual work happens. It takes the original image, follows the reverse-path instructions, and paints the new warped image. If a piece of the image gets stretched entirely off the canvas, it simply gets cut off. If there is empty space left over (for example, if the image shrank), it fills that empty background space with the color white. Finally, it uses the plotting tools to display the image on your screen, add your title to the top, and hide the grid lines so it looks clean.

Running the Loop
At the very bottom, outside of the recipe, the code actually sets everything into motion. It loads a sample photograph of an astronaut. It builds a list containing your five specific math matrices (A1 through A5). It then runs a loop, feeding the astronaut photo and one matrix at a time into the recipe, repeating the entire process five times to show you the five different visual results.
