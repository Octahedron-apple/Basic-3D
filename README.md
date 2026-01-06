# Basic-3D

**Basic-3D** is a lightweight Python project that demonstrates the fundamentals of 3D graphics programming. It generates 3D point-cloud shapes (cubes and spheres), applies mathematical transformations (rotation and translation), and projects them onto a 2D plane using perspective projection.

The project offers two modes of visualization:

1. **Video Generation**: Renders frames to images and compiles them into an MP4 video file using FFmpeg.
2. **Real-Time Rendering**: Renders the 3D animation live in a window using Tkinter.

## 📦 Requirements

### Python Libraries

This project requires Python 3 and the following external libraries:

* **NumPy**: Used for efficient matrix multiplication (rotation matrices) and vector arithmetic.
* **Pillow (PIL)**: Used by **Example 1 & 2** to draw projected points onto a canvas and save them as PNG images.
* **Tkinter**: Used by **Example 3** for real-time GUI rendering (usually included with standard Python installations).

### System Tools

* **FFmpeg**: Required **only for Example 1 and Example 2**. It is used to compile the sequence of rendered images into a video file.
* *Note: You must have `ffmpeg` installed on your system and added to your system's PATH for the video generation scripts to work.*



## ⚙️ Installation

1. **Clone the repository** (if applicable) or download the source files.
2. **Install Python Dependencies**:
Run the following command in your terminal to install `numpy` and `pillow`:
```bash
pip install -r requirements.txt

```


3. **Install FFmpeg** (Only if you plan to generate videos):
* **Linux (Debian/Ubuntu)**: `sudo apt install ffmpeg`
* **MacOS**: `brew install ffmpeg`
* **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add the `bin` folder to your System PATH variables.


4. **Tkinter Note (Linux Users)**:
If `example3.py` fails to run, you may need to install the Tkinter library manually:
```bash
sudo apt-get install python3-tk

```



## 🚀 How to Run

There are three example scripts provided to demonstrate different functionalities:

### 1. Real-Time Animation (`example3.py` and `example.py`)

This script creates a GUI window and renders a spinning cube in real-time. It does **not** require FFmpeg and does not save any files.

```bash
python3 example3.py
python3 example4.py
```

* **Behavior**: Opens a window titled "3D animation" displaying a rotating point-cloud cube.

### 2. Video Generation - Cube (`example1.py`)

Generates a 3D grid cube, rotates it around the X and Y axes, renders individual frames to an `Output` directory, and exports the animation as `exp1.mp4`.

```bash
python3 example1.py

```

### 3. Video Generation - Sphere (`example2.py`)

Similar to Example 1, but generates a 3D point-cloud sphere and exports the animation as `exp2.mp4`.

```bash
python3 example2.py

```
