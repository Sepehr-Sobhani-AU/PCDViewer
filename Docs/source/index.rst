.. PCDViewer documentation master file, created by
   sphinx-quickstart on Thu Nov 04 2024.

Welcome to PCDViewer's Documentation!
=====================================

PCDViewer is a lightweight, Qt-based OpenGL viewer designed for the efficient visualisation of point cloud data (PCD). This initial beta version is capable of handling midsize point clouds of up to approximately 100 million points, making it a useful tool for urban environments, geospatial analyses, and other projects involving detailed 3D spatial data. Whether you are a researcher, engineer, or enthusiast, PCDViewer provides essential tools to visualise and explore 3D data effectively.

Built with performance and simplicity in mind, PCDViewer supports basic operations like rotation, panning, zooming, and point selection. It offers adjustable parameters to give users more control over the visualisation, without unnecessary complexity. As a beta release, PCDViewer is still evolving and has room for further enhancements, especially in terms of its scalability and features.

PCDViewer is part of a larger project focused on point cloud analysis, classification, and feature detection using neural networks. Developers can easily embed `PCDViewerWidget` into their Python applications, making it a versatile component for visualising point clouds in broader workflows.

This documentation will help you start using the PCDViewer package, covering its modules, usage examples, and developer notes to customise its functionality for your specific needs.

Key Features
------------
- **Efficient Visualisation of Point Clouds**: PCDViewer is optimised to handle point clouds containing around 100 million points, balancing performance and responsiveness.
- **Interactive Controls**: Users can intuitively interact with point clouds, including zooming, panning, rotating, and selecting individual points.
- **Customisable Viewport**: PCDViewerWidget allows fine-tuning of the rendering process, such as setting the point size, adjusting axis visibility, and highlighting picked points.
- **OpenGL Powered**: By using OpenGL, PCDViewer ensures that rendering and interactions are fast and efficient, even for relatively large datasets.
- **Easy Integration**: The package can be easily integrated into other Python-based applications thanks to its lightweight nature and reliance on popular frameworks like Qt5 and OpenGL.

PCDViewerWidget Class Overview
------------------------------
The `PCDViewerWidget` class is the core component of the PCDViewer package. It is a specialised widget, based on Qt's `QOpenGLWidget`, designed specifically for rendering point clouds interactively. This class offers an immersive, interactive environment for viewing and exploring point cloud datasets.

The `PCDViewerWidget` class supports the following capabilities:

- **Point Cloud Rendering**: Render millions of 3D points efficiently, with options to assign RGB colour values to each point, thereby enhancing the data's visual clarity.
- **Interactive Camera Control**: Use mouse and keyboard inputs to rotate around the point cloud, zoom in and out, and pan across different sections of the data. The widget also supports resetting the camera view to its default state for convenience.
- **Point Picking**: Select individual points within the point cloud to highlight them, allowing for in-depth analysis or interactive exploration. The highlight colour and size can be customised to suit user preferences.
- **Axis Display**: Optionally display the X, Y, and Z axis lines within the viewport to provide a spatial reference. The length and thickness of these lines can be configured for clarity.
- **Versatile Visualisation**: Features such as adjustable point size, zoom sensitivity, rotation, and panning capabilities are provided to cater to different datasets and user requirements.
- **OpenGL Optimisation**: The widget uses OpenGL to handle the rendering pipeline efficiently, leveraging techniques such as Vertex Buffer Objects (VBOs) to ensure smooth interaction even with large datasets.

With `PCDViewerWidget`, developers can easily embed an interactive 3D visualisation tool into their Python applications, making it ideal for anyone working with spatial data, from environmental modellers to urban planners.

Documentation Overview
----------------------
This documentation aims to guide you through the different aspects of PCDViewer:

- **Modules**: Learn about the different modules that make up the PCDViewer package and understand how they contribute to the functionality of the tool.
- **Usage Examples**: See practical examples that show how to load and visualise point clouds, set up the viewer, and customise visualisation settings.
- **Developer Notes**: Detailed explanations are provided for extending and customising the functionality of `PCDViewerWidget` and integrating it into larger projects.


This introduction gives a fuller description of the PCDViewer package and the `PCDViewerWidget` class, emphasising its capabilities, key features, and the benefits to users. It is tailored for inclusion in the `index.rst` to help anyone new to the project understand its purpose and possibilities.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules
   example


Installation
------------
You can install the PCDViewer package using the `setup.py` file:

.. code-block:: bash

   # From package folder
   pip install .

or

.. code-block:: bash

   pip install pcdviewer

This command will install all the necessary dependencies and set up the package for use.

Quick Start
-----------
The following section provides a quick guide to start using PCDViewer.

.. code-block:: python

   from pcdviewer.PCDViewerWidget import PCDViewerWidget
   from PyQt5.QtWidgets import QApplication
   import numpy as np
   import sys

   # Create a 10,000 random point ndarray with float32 data type
   points = np.random.rand(10000, 3).astype(np.float32)
   colors = np.random.rand(10000, 3).astype(np.float32)

   # Initialize a Qt application
   app = QApplication(sys.argv)

   # Initialize PCDViewerWidget
   viewer = PCDViewerWidget()
   viewer.zoom_max_factor = 3
   viewer.default_zoom_factor = 1.5
   viewer.point_size = 2
   viewer.set_points(points, colors)
   viewer.show()

   # Execute the application
   sys.exit(app.exec_())


Hotkeys:
--------

- **Left Click**: Rotate around the X and Y axes.
- **CTRL + Left Click**: Rotate around the Z-axis.
- **Right/Middle Click**: Pan along the X and Y axes.
- **CTRL + Right/Middle Click**: Pan along the Z-axis.
- **Mouse Wheel**: Zoom in and out.
- **CTRL + R**: Reset the camera view to its default state.
- **SHIFT + Left Click**: Select a point in the point cloud.
- **SHIFT + Right Click**: Deselect a point in the point cloud.
- **ESC**: Deselect all selected points after confirmation.

Point Cloud Sample Files
------------------------

There is a sample point cloud data, in .ply and .npy file formats, containing 78,000,000 points. It can be loaded and visualised using the PCDViewer or the PCDViewerWidget.
Due to it's large size, the sample point cloud data is not included in the repository by default. However, you can download it from the following link:

-  `Download Example Files <https://drive.google.com/drive/folders/1OmusSVmtDM1ClJYEC_6n02--blED6aJY?usp=sharing>`_

Below is a list of files available:

-  `Toronto_Colors.ply`:  Point Cloud file suitable to load by PCDViewer.
-  `Toronto_Points.npy`:  Point Cloud coordinates in numpy ndarray format, suitable to use by PCDViewerWidget.
-  `Toronto_Colors.npy`:  Point Cloud colour in numpy ndarray format, suitable to use by PCDViewerWidget.

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

