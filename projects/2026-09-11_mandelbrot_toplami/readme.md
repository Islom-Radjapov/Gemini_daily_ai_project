# mandelbrot_explorer

## Project Name: Mandelbrot Explorer

## Description:
Mandelbrot Explorer is a small, interactive web application that allows users to explore the beautiful and intricate Mandelbrot set. It renders the fractal directly on an HTML5 canvas and provides controls for zooming, panning, and adjusting the calculation's detail level using both mouse and keyboard inputs. The entire project is contained within a single HTML file, adhering to the requested "single-file application" constraint.

## How to Run:
1.  **Save the file:** Copy the content of `index.html` into a new file named `index.html` on your computer.
2.  **Open in browser:** Open the `index.html` file with any modern web browser (e.g., Chrome, Firefox, Edge, Safari).
3.  **Start Exploring:** The Mandelbrot set will be rendered immediately, and you can start interacting with it.

## Features List:
*   **Mandelbrot Set Rendering:** Renders the classic Mandelbrot fractal using an iterative algorithm.
*   **Interactive Zoom:**
    *   **Mouse Scroll:** Zoom in or out at the precise location of your mouse cursor.
    *   **'+' / '-' Keys:** Zoom in or out at the center of the current view.
*   **Interactive Panning:**
    *   **Click & Drag (Mouse):** Pan the view by clicking and dragging the canvas.
    *   **Arrow Keys:** Pan the view up, down, left, or right.
*   **Iteration Control:**
    *   **'I' Key:** Increase the maximum number of iterations, allowing for more detailed rendering of complex areas (may slow down rendering).
    *   **'D' Key:** Decrease the maximum number of iterations (speeds up rendering, but loses detail).
*   **Reset View:** Press the **'R' key** to instantly return to the initial, wide view of the Mandelbrot set.
*   **Smooth Coloring:** Employs a smooth coloring algorithm based on the number of iterations to produce visually appealing gradients.
*   **Single File:** All HTML, CSS, and JavaScript are contained within `index.html` for easy deployment and portability.
*   **Responsive Canvas:** The canvas resolution is fixed, but its display size adapts to a degree with CSS, while maintaining proper aspect ratio for calculations.
*   **Clean and Modern Design:** A dark theme with clear controls provides a pleasant user experience.