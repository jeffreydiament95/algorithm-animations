**Create conda env**
conda create -n manim-env
conda activate manim-env
conda install -c conda-forge manim
conda install -c conda-forge pycairo
conda install -c conda-forge pygments

**Run code**
conda activate manim-env
manim {python file} {Manim class}

common flags:
-p to automatically open the video file once it's ready
-ql, -qm, qh, q4 for low, medium, high, 4k video quality

for example: manim -p -ql binary_search.py BinarySearch


