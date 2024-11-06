# PCDViewer

**PCDViewer** is a lightweight, Qt-based OpenGL viewer designed to visualise midsize point cloud datasets with ease. This package allows users to work with point clouds of approximately 100 million points, making it suitable for applications such as urban planning, geospatial analysis, and environmental monitoring. It is part of a larger project aimed at point cloud analysis, classification, and feature detection using neural networks, which is under development.

## Features

- Efficiently visualises midsize point clouds (\~100 million points).
- Qt-based OpenGL rendering for interactive 3D visualisation.
- Supports operations like rotation, panning, zooming, and point picking.
- Adjustable parameters for optimised point cloud interaction.
- Easy integration as a widget in custom Python projects.

## Requirements

- Python 3.8 or above
- PyQt5
- numpy
- OpenGL
- open3d (optional, for file import)

## Installation

You can install **PCDViewer** via pip:

```sh
pip install pcdviewer
```

Alternatively, you can clone the repository and install the package manually:

```sh
git clone https://github.com/Sepehr-Sobhani-AU/PCDViewer.git
cd PCDViewer
python setup.py install
```

## Usage

**PCDViewer** provides a main widget called `PCDViewerWidget` that can be used in PyQt5 applications for visualising point clouds.

### Example Usage

Here's an example of how to create a PyQt5 application that uses `PCDViewerWidget` to visualise a point cloud:

```python
from pcdviewer.PCDViewerWidget import PCDViewerWidget
from PyQt5.QtWidgets import QApplication
import numpy as np
import sys

# Create a 10,000 random point ndarray with float32 data type
points = np.random.rand(10000, 3).astype(np.float32)
colors = np.random.rand(10000, 3).astype(np.float32)

# Initialise a Qt application
app = QApplication(sys.argv)

# Initialise PCDViewerWidget
viewer = PCDViewerWidget()
viewer.zoom_max_factor = 3
viewer.default_zoom_factor = 1.5
viewer.point_size = 2
viewer.set_points(points, colors)
viewer.show()

# Execute the application
sys.exit(app.exec_())
```

### Example File Loader

To load a point cloud from a `.ply` file using Open3D:

```python
import sys
from PyQt5 import QtWidgets
import numpy as np
import open3d as o3d
from pcdviewer.PCDViewerWidget import PCDViewerWidget

def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    main_window.setWindowTitle("PCDViewerWidget Example")
    main_window.resize(800, 600)

    central_widget = QtWidgets.QWidget()
    main_window.setCentralWidget(central_widget)

    layout = QtWidgets.QVBoxLayout(central_widget)
    viewer_widget = PCDViewerWidget(central_widget)
    layout.addWidget(viewer_widget)

    # Load point cloud data
    pcd_data = o3d.io.read_point_cloud("path/to/your/pointcloud.ply")
    points = np.asarray(pcd_data.points, dtype=np.float32)
    colors = np.asarray(pcd_data.colors, dtype=np.float32) if pcd_data.colors else None
    viewer_widget.set_points(points, colors)

    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
```

## Documentation

For detailed documentation, refer to the `Docs` folder or visit the [GitHub Pages](https://github.com/Sepehr-Sobhani-AU/PCDViewer/Docs). The documentation includes detailed information about modules, classes, methods, and properties available in the package, including how to extend and customise the widget.

## Contributing

Contributions are welcome! Whether it's bug reports, feature requests, or pull requests, feel free to contribute and help improve PCDViewer. Please ensure all contributions adhere to the style guide and best practices detailed in the `CONTRIBUTING.md`.

## Roadmap

**PCDViewer** is in its initial release (beta version). We have plans to improve its capabilities further, such as:

- **Out-of-Core Rendering:** To enable visualisation of extremely large point clouds.
- **Classification and Feature Detection:** Part of the broader vision to integrate neural network-based classification and analysis tools.
- **GUI Enhancements:** More user-friendly tools and interaction modes for enhanced productivity.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For any questions, feel free to reach out via GitHub or send an email to [sepehr.sobhani@gmail.com](mailto\:sepehr.sobhani@gmail.com).

