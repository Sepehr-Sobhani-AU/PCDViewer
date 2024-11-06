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
