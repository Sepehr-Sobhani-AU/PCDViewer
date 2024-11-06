from PyQt5 import QtCore, QtGui, QtWidgets
from pcdviewer.PCDViewerWidget import PCDViewerWidget
import numpy as np
import open3d as o3d

class Ui_MainWindow(object):
    """
    The `Ui_MainWindow` class defines the user interface of the main application window, which serves as a graphical
    interface for visualising point cloud data using the PCDViewerWidget.

    The class uses PyQt5 to create the main window layout, including a menu bar, status bar, and a central widget that
    embeds a 3D OpenGL-based viewer for point clouds. The viewer allows users to interact with the point cloud data,
    providing an intuitive way to explore and visualise the content.

    Attributes:
    -----------
    centralwidget : QtWidgets.QWidget
        The central widget for the main window, which contains all the main UI components.
    main_layout : QtWidgets.QVBoxLayout
        Layout used to organise the PCDViewerWidget within the central widget.
    openGLWidget : PCDViewerWidget
        Custom widget for viewing point cloud data using OpenGL.
    menubar : QtWidgets.QMenuBar
        Menu bar of the main window, containing File and Help menus.
    menuFile : QtWidgets.QMenu
        "File" menu containing actions such as opening files.
    menuHelp : QtWidgets.QMenu
        "Help" menu for additional actions (currently empty).
    statusbar : QtWidgets.QStatusBar
        Status bar for the main window, used to display status information.
    actionOpen : QtWidgets.QAction
        Action to open a point cloud file, used in the File menu.
 """
    def setupUi(self, MainWindow):
        """
        Set up the user interface for the main window.

        This method is called to create and arrange all the components within the main window, including the menu bar,
        status bar, the central widget with the OpenGL-based PCDViewerWidget, and actions for interacting with the point
        cloud data.

        Args:
            MainWindow (QMainWindow): The main window instance to which this UI is applied.
        """
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setWindowTitle("PCD Visualiser")

        # Create the central widget
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Set the central widget for MainWindow
        MainWindow.setCentralWidget(self.centralwidget)

        # Create a layout for the central widget
        self.main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)  # Set margins to control positioning

        # Create the PCDViewerWidget
        self.openGLWidget = PCDViewerWidget(self.centralwidget)
        self.openGLWidget.setObjectName("openGLWidget")

        # Add the PCDViewerWidget to the main layout
        self.main_layout.addWidget(self.openGLWidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.menuFile.addAction(self.actionOpen)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Connect the "Open" action to the function that opens the file dialog
        self.actionOpen.triggered.connect(self.open_file_dialog)

    def retranslateUi(self, MainWindow):
        """
        Set the display text for the user interface elements.

        This method is used to set the text for various UI components, including the menu titles and actions.

        Args:
            MainWindow (QMainWindow): The main window instance to which this UI is applied.
        """
        _translate = QtCore.QCoreApplication.translate
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))

    def open_file_dialog(self):
        """
        Open a file dialog to select a `.ply` point cloud file.

        This method allows the user to select a `.ply` file, which is then loaded using the Open3D library. The loaded
        point cloud data is converted to NumPy arrays for points and colors, and these arrays are passed to the
        PCDViewerWidget for visualisation.
        """

        # Open a file dialog to select a .ply file
        options = QtWidgets.QFileDialog.Options()
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            None,
            "Open PLY File",
            "",
            "PLY Files (*.ply);;All Files (*)",
            options=options
        )

        if file_path:
            # Load the .ply file using open3d
            pcd_data = o3d.io.read_point_cloud(file_path)

            # Convert to numpy arrays
            points = np.asarray(pcd_data.points, dtype=np.float32)
            colors = np.asarray(pcd_data.colors, dtype=np.float32) if pcd_data.colors else None

            # Set the points and colors in the PCDViewerWidget
            self.openGLWidget.set_points(points, colors)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    sys.exit(app.exec_())
