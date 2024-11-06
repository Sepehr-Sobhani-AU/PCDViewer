# This is the example code to explain how to use the PCDViewerWidget in a PyQt5 application.
# The example code creates a simple Qt application with a QMainWindow and a PCDViewerWidget.
# The PCDViewerWidget is populated with some sample points and colors.
# The example code can be run by executing the Example.py file.

import sys
from PyQt5 import QtWidgets
import numpy as np

# Import the PCDViewerWidget class from the PCDViewerWidget.py module in the pcdviewer package
from pcdviewer.PCDViewerWidget import PCDViewerWidget

def main():
    """Main function for the example code."""

    # Create a Qt application
    app = QtWidgets.QApplication(sys.argv)

    # Create the main window
    main_window = QtWidgets.QMainWindow()
    main_window.setWindowTitle("PCDViewerWidget Example")
    main_window.resize(800, 600)

    # Create the central widget
    central_widget = QtWidgets.QWidget()
    main_window.setCentralWidget(central_widget)

    # Create a layout and add the PCDViewerWidget
    layout = QtWidgets.QVBoxLayout(central_widget)
    viewer_widget = PCDViewerWidget(central_widget)
    layout.addWidget(viewer_widget)

    # Set some sample points for the PCDViewerWidget

    sample_points = np.load("Toronto_Points.npy").astype(np.float32)
    sample_colors = np.load("Toronto_Colors.npy").astype(np.float32)
    viewer_widget.set_points(sample_points, sample_colors)

    # Show the main window
    main_window.show()

    # Execute the application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
