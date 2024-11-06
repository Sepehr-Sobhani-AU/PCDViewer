PCDViewer Examples
==================

This page provides two example usages of the PCDViewer package to help users get started.

Example1 Script
---------------

This example demonstrates how to use the `PCDViewerWidget` in a PyQt5 application for visualising point cloud data.
The script creates a simple PyQt5 application consisting of a `PCDViewerWidget` where users can visualise randomly
generated 3D point cloud data.

Key Components of the Example1
------------------------------

1. **Point Cloud Generation**:
    The example generates 10,000 random 3D points (`points`) and assigns random RGB colors (`colors`). These points
    are represented as a NumPy array with a `float32` data type.

2. **Creating the Qt Application**:
    A `QApplication` is created, which is required to run the Qt application. The main application is executed
    through `sys.argv`.

3. **Initialising the PCDViewerWidget**:
    An instance of the `PCDViewerWidget` is created and customised:
        - `zoom_max_factor` is set to `3` to limit the maximum zoom level.
        - `default_zoom_factor` is set to `1.5` to specify the initial zoom level.
        - `point_size` is set to `2` to make the points larger for better visibility.
        - The `set_points()` method is used to set the randomly generated points and their corresponding colors to the viewer.

4. **Launching the Application**:
    The `PCDViewerWidget` is displayed by calling the `show()` method, and the Qt application enters its main event loop
    with `app.exec_()`.

This example serves as a starting point to integrate the `PCDViewerWidget` into larger applications, where users can
visualise their point cloud data in an interactive 3D viewer.

.. literalinclude:: ../../Example/Example1.py
   :language: python
   :linenos:

----------------------------------------------------------------------------------------------------------------------------

Example2 Script
---------------

This example demonstrates how to use the `PCDViewerWidget` in a PyQt5 application with a main window for visualising 
real-world point cloud data. The script creates a PyQt5 `QMainWindow` containing a `PCDViewerWidget` to display 
the 3D point cloud.
The following script shows how to load `.npy` files and use the PCDViewerWidget to visualise the point cloud data.

Point Cloud Sample Files
------------------------

There is a sample point cloud data, in .ply and .npy file formats, containing 78,000,000 points. It can be loaded and visualised using the PCDViewer or the PCDViewerWidget.
Due to it's large size, the sample point cloud data is not included in the repository by default. However, you can download it from the following link:

-   `Download Example Files <https://drive.google.com/drive/folders/1OmusSVmtDM1ClJYEC_6n02--blED6aJY?usp=sharing>`_

Below is a list of files available:

-   `Toronto_Colors.ply`:  Point Cloud file suitable to load by PCDViewer.
-   `Toronto_Points.npy`:  Point Cloud coordinates in numpy ndarray format, suitable to use by PCDViewerWidget.
-   `Toronto_Colors.npy`:  Point Cloud colour in numpy ndarray format, suitable to use by PCDViewerWidget.

Key Components of the Example2
------------------------------

1. **Application Window Setup**:
    - The script creates a main window (`QMainWindow`) with a central widget and layout using PyQt5.
    - The window is titled `"PCDViewerWidget Example"` and is set to a default size of `800x600`.

2. **Point Cloud Data Loading**:
    - Real-world point cloud data of Toronto is loaded using NumPy from `.npy` files (`Toronto_Points.npy` and `Toronto_Colors.npy`).
    - These files contain 3D coordinates (`sample_points`) and RGB colors (`sample_colors`) of the point cloud.
    - The loaded data is converted to a `float32` data type to ensure compatibility with the `PCDViewerWidget`.

3. **Adding PCDViewerWidget to the Layout**:
    - The `PCDViewerWidget` is instantiated and added to the layout of the central widget.
    - The point cloud data is visualised by using the `set_points()` method of the `PCDViewerWidget`.

4. **Launching the Application**:
    - The `main_window` is shown, and the application enters its main event loop via `app.exec_()`.

This example can be used as a reference for integrating the `PCDViewerWidget` into a larger PyQt5-based GUI application, 
where users can visualise detailed point cloud data interactively.

.. literalinclude:: ../../Example/Example2.py
   :language: python
   :linenos: