# Basic-3D
# Basic-3D

**Basic-3D** is a lightweight Python project that demonstrates the fundamentals of 3D graphics programming. It generates 3D point-cloud shapes (cubes and spheres), applies mathematical transformations (rotation and translation), projects them onto a 2D plane using perspective projection, and renders the result as an animation.

## 📦 Requirements

### Python Libraries
This project requires Python 3 and the following external libraries:
* **NumPy**: Used for efficient matrix multiplication (rotation matrices) and vector arithmetic.
* **Pillow (PIL)**: Used to draw the projected 2D points onto a canvas and save them as PNG images.

### System Tools
* **FFmpeg**: This project relies on FFmpeg to compile the sequence of rendered images into a video file.
    * *Note: You must have `ffmpeg` installed on your system and added to your system's PATH for the scripts to work.*

## ⚙️ Installation

1.  **Clone the repository** (if applicable) or download the source files.
2.  **Install Python Dependencies**:
    Run the following command in your terminal to install `numpy` and `pillow`:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Install FFmpeg**:
    * **Linux (Debian/Ubuntu)**: `sudo apt install ffmpeg`
    * **MacOS**: `brew install ffmpeg`
    * **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add the `bin` folder to your System PATH variables.

## 🚀 How to Run

There are two example scripts provided to demonstrate the functionality:

### 1. Rotating Cube (`example1.py`)
Generates a 3D grid cube, rotates it around the X and Y axes, and exports the animation.

```bash
python3 example1.py
