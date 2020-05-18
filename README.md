# AMOSA-Clustering-for-Eyes

This project is the next step of the project started here (https://github.com/Noahkito/Face-Feature-Classification). It takes a collection of eye crops and a collection of clustering files associated with those eye crops. Place each of the eye crops into /all/ before running the code.

# Installation

Download Anaconda (https://www.anaconda.com/products/individual)

run the following commands

> conda create --name eyes

> conda install -n eyes python=3.7.6 scipy

> conda activate eyes

> pip install opencv-python cmake dlib imutils matplotlib cython pillow networkx

With this, your virtual environment is set up for this project.

# Usage

> python vote.py

This will move every eye crop from the /all/ folder into a numbered folder representing their clustered group.

> python analysis.py

This will give demographic information regarding every cluster group.
