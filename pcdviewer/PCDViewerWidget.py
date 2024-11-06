import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget, QMessageBox
from PyQt5.QtCore import Qt, QTimer
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective,gluProject, gluUnProject
from OpenGL.GLU import gluNewQuadric, gluDeleteQuadric, gluQuadricDrawStyle
from OpenGL.GLU import gluSphere
from OpenGL.GLU import GLU_LINE, GLU_FILL
from OpenGL.arrays import vbo

class PCDViewerWidget(QOpenGLWidget):
    """
    A Qt-based OpenGL widget for viewing point cloud data (PCD).

    This class provides an interactive visualisation environment for point clouds, allowing for operations such as
    rotation, panning, zooming, and point selection. It leverages OpenGL for efficient rendering of large point
    clouds and supports advanced features such as axis symbol display, point picking, and modifying the centre of
    rotation.

    Hotkeys:
        - Left Click: Rotate around the X and Y axes.
        - CTRL + Left Click: Rotate around the Z-axis.
        - Right/Middle Click: Pan along the X and Y axes.
        - CTRL + Right/Middle Click: Pan along the Z-axis.
        - Mouse Wheel: Zoom in and out.
        - CTRL + R: Reset the camera view to its default state.
        - SHIFT + Left Click: Select a point in the point cloud.
        - SHIFT + Right Click: Deselect a point in the point cloud.
        - ESC: Deselect all selected points after confirmation.

    Attributes:
    -----------
        The following attributes represent internal state variables that are used in the widget's logic and operations. They are not intended to be directly accessed or modified by users of this class, but instead are used internally to maintain the state of the viewer and perform necessary computations.

        - center (numpy.ndarray): Centre of the current point cloud.
        - size (numpy.ndarray): Size of the bounding box of the point cloud.
        - max_extent (float): Maximum extent of the point cloud's bounding box.
        - fov (float): Field of view (in degrees) of the perspective camera.
        - near_plane (float): Distance to the near clipping plane.
        - far_plane (float): Distance to the far clipping plane.
        - points (numpy.ndarray): Point cloud data including positions and optional colours.
        - vbo (vbo.VBO): Vertex buffer object for efficient rendering of point cloud data.
        - last_mouse_pos (QPoint): Last recorded mouse position for interaction.
        - rot_x (float): Rotation angle around the X-axis.
        - rot_y (float): Rotation angle around the Y-axis.
        - rot_z (float): Rotation angle around the Z-axis.
        - pan_x (float): Panning offset along the X-axis.
        - pan_y (float): Panning offset along the Y-axis.
        - pan_z (float): Panning offset along the Z-axis.
        - is_rotating (bool): Flag to indicate if the widget is in rotation mode.
        - is_rotating_z (bool): Flag to indicate if the widget is rotating around the Z-axis.
        - is_panning (bool): Flag to indicate if the widget is in panning mode.
        - is_panning_z (bool): Flag to indicate if the widget is panning along the Z-axis.
        - show_axis (bool): Flag to indicate whether the axis symbol should be displayed.
        - picked_points_indices (list of int): List of indices of picked points from the point cloud.
        - model_view_matrix (numpy.ndarray): Model-view matrix for the current OpenGL context.
        - projection_matrix (numpy.ndarray): Projection matrix for the current OpenGL context.
        - viewport (numpy.ndarray): Viewport settings for the OpenGL context.
        - camera_distance (float): Current distance of the camera from the point cloud.
        - axis_timer (QTimer or None): Timer for hiding the axis symbol after panning.

    """

    @property
    def point_size(self):
        """
        float: Size of the rendered points. Can be set to adjust point cloud visibility.
        """
        return self._point_size

    @point_size.setter
    def point_size(self, value):
        if value > 0:
            self._point_size = value
            self.update()

    @property
    def axis_line_length(self):
        """
        float: Length of the axis lines for the axis symbol. Can be set to adjust axis visibility.
        """
        return self._axis_line_length

    @axis_line_length.setter
    def axis_line_length(self, value):
        if value > 0:
            self._axis_line_length = value
            self.update()

    @property
    def axis_line_width(self):
        """
        float: Width of the axis lines for the axis symbol. Can be set to adjust axis visibility.
        """
        return self._axis_line_width

    @axis_line_width.setter
    def axis_line_width(self, value):
        if value > 0:
            self._axis_line_width = value
            self.update()

    @property
    def picking_point_threshold_factor(self):
        """
        float: Threshold factor for determining if a point can be picked. Can be adjusted for selection precision.
        """
        return self._picking_point_threshold_factor

    @picking_point_threshold_factor.setter
    def picking_point_threshold_factor(self, value):
        if value > 0:
            self._picking_point_threshold_factor = value

    @property
    def picked_point_highlight_color(self):
        """
        tuple of float: RGB colour for highlighting picked points. Can be set to customise highlight colour.
        """
        return self._picked_point_highlight_color

    @picked_point_highlight_color.setter
    def picked_point_highlight_color(self, value):
        if len(value) == 3 and all(0.0 <= v <= 1.0 for v in value):
            self._picked_point_highlight_color = value
            self.update()

    @property
    def picked_point_highlight_size(self):
        """
        float: Size factor for rendering picked points as highlighted spheres. Can be set to adjust highlight size.
        """
        return self._picked_point_highlight_size

    @picked_point_highlight_size.setter
    def picked_point_highlight_size(self, value):
        if value > 0:
            self._picked_point_highlight_size = value
            self.update()

    @property
    def zoom_min_factor(self):
        """
        float: Minimum zoom factor limit. Can be adjusted to control zoom limits.
        """
        return self._zoom_min_factor

    @zoom_min_factor.setter
    def zoom_min_factor(self, value):
        if value > 0:
            self._zoom_min_factor = value

    @property
    def zoom_max_factor(self):
        """
        float: Maximum zoom factor limit. Can be adjusted to control zoom limits.
        """
        return self._zoom_max_factor

    @zoom_max_factor.setter
    def zoom_max_factor(self, value):
        if value > self._zoom_min_factor:
            self._zoom_max_factor = value

    @property
    def zoom_sensitivity(self):
        """
        float: Sensitivity of the zoom operation. Can be adjusted to control zoom speed.
        """
        return self._zoom_sensitivity

    @zoom_sensitivity.setter
    def zoom_sensitivity(self, value):
        if value > 0:
            self._zoom_sensitivity = value

    @property
    def pan_sensitivity(self):
        """
        float: Sensitivity of the panning operation. Can be adjusted to control panning speed.
        """
        return self._pan_sensitivity

    @pan_sensitivity.setter
    def pan_sensitivity(self, value):
        if value > 0:
            self._pan_sensitivity = value

    @property
    def rotate_sensitivity(self):
        """
        float: Sensitivity of the rotation operation. Can be adjusted to control rotation speed.
        """
        return self._rotate_sensitivity

    @rotate_sensitivity.setter
    def rotate_sensitivity(self, value):
        if value > 0:
            self._rotate_sensitivity = value

    @property
    def pixel_threshold(self):
        """
        int: Threshold (in pixels) for selecting/deselecting points in screen space. Can be set to adjust selection accuracy.
        """
        return self._pixel_threshold

    @pixel_threshold.setter
    def pixel_threshold(self, value):
        if value > 0:
            self._pixel_threshold = value

    @property
    def default_camera_distance(self):
        """
        float: Default distance of the camera from the point cloud. Can be set to adjust the initial camera view.
        """
        return self._default_camera_distance

    @default_camera_distance.setter
    def default_camera_distance(self, value):
        self._default_camera_distance = value

    @property
    def default_zoom_factor(self):
        """
        float: Default zoom factor for the camera. Can be set to adjust the initial zoom level.
        """
        return self._default_zoom_factor

    @default_zoom_factor.setter
    def default_zoom_factor(self, value):
        self._default_zoom_factor = value

    @property
    def default_rot_x(self):
        """
        float: The current value of the default rotation around the X-axis.
        """
        return self._default_rot_x

    @default_rot_x.setter
    def default_rot_x(self, value):
        self._default_rot_x = value

    @property
    def default_rot_y(self):
        """
        float: The current value of the default rotation around the Y-axis.
        """
        return self._default_rot_y

    @default_rot_y.setter
    def default_rot_y(self, value):
        self._default_rot_y = value

    @property
    def default_rot_z(self):
        """
        float: The current value of the default rotation around the Z-axis.
        """
        return self._default_rot_z

    @default_rot_z.setter
    def default_rot_z(self, value):
        self._default_rot_z = value

    @property
    def default_pan_x(self):
        """
        float: The current value of the default pan along the X-axis.
        """
        return self._default_pan_x

    @default_pan_x.setter
    def default_pan_x(self, value):
        self._default_pan_x = value

    @property
    def default_pan_y(self):
        """
        float: The current value of the default pan along the Y-axis.
        """
        return self._default_pan_y

    @default_pan_y.setter
    def default_pan_y(self, value):
        self._default_pan_y = value

    @property
    def default_pan_z(self):
        """
        float: The current value of the default pan along the Z-axis.
        """
        return self._default_pan_z

    @default_pan_z.setter
    def default_pan_z(self, value):
        self._default_pan_z = value

    def __init__(self, parent=None):
        super().__init__()

        # Set focus policy to ensure the widget receives keyboard events
        self.setFocusPolicy(Qt.StrongFocus)

        # Initialize variables for zoom to extent
        self.center = np.array([0.0, 0.0, 0.0])
        self.size = np.array([1.0, 1.0, 1.0])
        self.max_extent = None
        self.fov = 60.0  # Field of view in degrees
        self.near_plane = 0.1
        self.far_plane = 1000.0

        self.points = None
        self.vbo = None

        # Interaction variables
        self.last_mouse_pos = None

        self.rot_x = 0.0  # Rotation around X-axis
        self.rot_y = 0.0  # Rotation around Y-axis
        self.rot_z = 0.0  # Rotation around Z-axis

        self.pan_x = 0.0  # Panning along X-axis
        self.pan_y = 0.0  # Panning along Y-axis
        self.pan_z = 0.0  # Panning along Z-axis

        # Interaction flags
        self.is_rotating = False
        self.is_rotating_z = False  # New flag for Z-axis rotation
        self.is_panning = False
        self.is_panning_z = False  # New flag for Z-axis panning
        self.show_axis = False  # Flag to show/hide the axis symbol

        # Initialize list to store indices of picked points
        self.picked_points_indices = []

        # Initialize matrices used in the pick_point method
        self.model_view_matrix = np.identity(4)
        self.projection_matrix = np.identity(4)
        self.viewport = np.array([0, 0, self.width(), self.height()], dtype=np.int32)

        # Setting properties as attributes that can be adjusted
        self._point_size = 0.5
        self._axis_line_length = 5
        self._axis_line_width = 5
        self._picking_point_threshold_factor = 1.0
        self._picked_point_highlight_color = (1.0, 0.0, 0.0)
        self._picked_point_highlight_size = 1
        self._zoom_min_factor = 0.02
        self._zoom_max_factor = 1
        self._zoom_sensitivity = 1
        self._pan_sensitivity = 1
        self._rotate_sensitivity = 1
        self._pixel_threshold = 5

        # Properties for the attributes
        self._default_camera_distance = None
        self._default_zoom_factor = self._zoom_max_factor
        self._default_rot_x = 0.0
        self._default_rot_y = 0.0
        self._default_rot_z = 0.0
        self._default_pan_x = 0.0
        self._default_pan_y = 0.0
        self._default_pan_z = 0.0

        # Initialize default values
        self.camera_distance = None
        self.zoom_factor = self._default_zoom_factor

        # Timer for hiding the axis symbol after panning
        self.axis_timer = None

    def initializeGL(self):
        """
        Initialise the OpenGL context for the widget.

        This method sets up the OpenGL environment, including clearing the background colour, enabling depth testing,
        and setting up blending options for transparency.

        Raises:
            ValueError: If the point cloud data (points) is not set before initialisation.
        """

        # OpenGL initialization
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def initialize_view(self):
        """
        Initialize the camera and view settings for the new point cloud.

        This method sets the default camera distance, pan, and zoom values
        after new point cloud data has been set.
        """

        # Zoom extent
        # Calculate center, size, and max extent
        min_bounds = self.points.min(axis=0)
        max_bounds = self.points.max(axis=0)
        self.center = (min_bounds + max_bounds) / 2.0
        self.size = max_bounds - min_bounds
        self.max_extent = self.size.max()

        # Calculate initial camera distance
        half_fov_rad = np.radians(self.fov / 2)
        self.default_camera_distance = self.max_extent / (2 * np.tan(half_fov_rad)) * 1.2  # Include padding factor
        self.camera_distance = self.default_camera_distance

        # Pan the camera to the center of the point cloud
        self.default_pan_x = -self.center[0]
        self.default_pan_y = -self.center[1]
        self.default_pan_z = -self.center[2]
        self.pan_x = self.default_pan_x
        self.pan_y = self.default_pan_y
        self.pan_z = self.default_pan_z

        # Set near and far planes based on the new camera distance
        self.near_plane = max(self.camera_distance - self.max_extent * 2, 0.1)  # Ensure near plane is positive
        self.far_plane = self.camera_distance + self.max_extent * 2

        # Reset zoom factor
        self.zoom_factor = self.default_zoom_factor

        # Trigger a redraw to reflect the updated point cloud
        self.update()

    def set_points(self, points: np.ndarray, colors: np.ndarray = None):
        """
        Set the point cloud data to be visualised in the widget.

        This method accepts point coordinates and optional colour information. It also initialises
        the vertex buffer object (VBO) with the given data.

        Args:
            points (numpy.ndarray): A Nx3 array of point coordinates (x, y, z). Must be of type float32.
            colors (numpy.ndarray, optional): A Nx3 array of RGB colour values corresponding to each point.
                Must be of type float32. If not provided, all points will be rendered with a default colour.

        Raises:
            AssertionError: If the `points` array does not have the correct shape or data type.
            AssertionError: If the `colors` array is provided but does not have the correct shape or data type.
        """
        assert points.shape[1] == 3, "Points array must have shape Nx3"
        assert points.dtype == np.float32, "Points array must be of type float32"

        if colors is not None:
            assert points.shape[0] == colors.shape[0], "Points and colors must have the same number of entries"
            assert colors.shape[1] == 3, "Colors array must have shape Nx3"
            assert colors.dtype == np.float32, "Colors array must be of type float32"

        # Extract colors
        if colors is None:
            colors = np.ones_like(points).astype(np.float32)

        self.points = np.hstack((points, colors)).astype(np.float32)

        # Invalidate the existing VBO if it exists, as the points have changed
        if self.vbo is not None:
            self.vbo.delete()
            self.vbo = None

        # Initialize the view after setting points
        self.initialize_view()

    def draw_axis_symbol(self, position):
        """
        Draw the axis symbol at the specified position.

        This method renders a 3D axis symbol, consisting of X, Y, and Z axes, at the given position in the point cloud
        space. The X-axis is rendered in red, the Y-axis in green, and the Z-axis in blue. This symbol is used to help
        users orient themselves within the point cloud.

        Args:
            position (tuple or list or numpy.ndarray): A 3-element array representing the (x, y, z) position where
                the axis symbol should be drawn.
        """

        glPushMatrix()

        glLineWidth(self.axis_line_width)
        glTranslatef(position[0], position[1], position[2])

        glBegin(GL_LINES)
        # X-axis in red
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(self.axis_line_length, 0.0, 0.0)

        # Y-axis in green
        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, self.axis_line_length, 0.0)

        # Z-axis in blue
        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, 0.0, self.axis_line_length)
        glEnd()

        glLineWidth(self.axis_line_width)

        glPopMatrix()

    def paintGL(self):
        """
        Render the point cloud and other visual elements.

        This method is called whenever the widget needs to be repainted. It clears the colour and depth buffers, sets
        up the projection and model-view matrices, and renders the point cloud data, picked points, and optionally the
        axis symbol. The rendering includes applying transformations for panning, zooming, and rotation.

        If no point cloud data is set, the method returns without rendering anything.
        """

        if self.points is None or self.max_extent is None:
            return

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Update projection matrix
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        w = self.width()
        h = self.height()
        aspect = w / h if h != 0 else 1
        gluPerspective(self.fov * self.zoom_factor, aspect, max(self.near_plane, 0.1), self.far_plane)

        # Update model-view matrix
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # Move the camera back
        camera_distance = self.camera_distance * self.zoom_factor
        glTranslatef(0.0, 0.0, -camera_distance)

        # Apply panning
        glTranslatef(self.pan_x, self.pan_y, self.pan_z)

        # Translate to the center of rotation
        glTranslatef(self.center[0], self.center[1], self.center[2])

        # Apply rotations around the origin
        glRotatef(self.rot_x, 1.0, 0.0, 0.0)
        glRotatef(self.rot_y, 0.0, 1.0, 0.0)
        glRotatef(self.rot_z, 0.0, 0.0, 1.0)

        # Translate back from the center
        glTranslatef(-self.center[0], -self.center[1], -self.center[2])

        # Render the point cloud
        self.render_point_cloud()

        # Render picked points
        self.render_picked_points()

        # Store matrices for picking
        self.model_view_matrix = glGetDoublev(GL_MODELVIEW_MATRIX).copy()
        self.projection_matrix = glGetDoublev(GL_PROJECTION_MATRIX).copy()
        self.viewport = glGetIntegerv(GL_VIEWPORT).copy()

        # Draw the point of view (POV) sphere
        if self.show_axis:
            # Draw axis symbol at the center of rotation
            self.draw_axis_symbol(self.center)

    def render_point_cloud(self):
        """
        Render the point cloud data.

        This method is responsible for rendering the point cloud using OpenGL. It enables the necessary client states,
        binds the vertex buffer object (VBO), and sets the appropriate pointers for vertex and colour data. After
        rendering the points, the method disables the client states.

        The point cloud is rendered as a series of GL_POINTS, and each point's colour is determined by the VBO data.
        """

        if self.points is None:
            return

        # Create and bind the VBO if it's not already created
        if self.vbo is None:
            self.vbo = vbo.VBO(self.points)

        #glEnable(GL_POINT_SMOOTH)
        glPointSize(self.point_size)

        # Enable client states
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)

        # Bind the VBO
        self.vbo.bind()

        # Set pointers to the VBO data
        stride = 6 * self.points.itemsize
        glVertexPointer(3, GL_FLOAT, stride, self.vbo)
        glColorPointer(3, GL_FLOAT, stride, self.vbo + 12)

        # Draw all points
        glDrawArrays(GL_POINTS, 0, len(self.points))

        # Disable client states
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)

    def render_picked_points(self):
        """
        Render the picked points in the point cloud.

        This method highlights the picked points by drawing spheres at their positions. The colour and size of the
        spheres are determined by the `picked_point_highlight_color` and `picked_point_highlight_size` attributes.
        The purpose of this method is to visually distinguish the picked points from the rest of the point cloud.

        If no points have been picked, the method returns without rendering anything.
        """

        # Highlight picked points by drawing spheres
        if self.picked_points_indices:
            glColor3f(*self.picked_point_highlight_color)

            for index in self.picked_points_indices:
                position = self.points[index, :3]

                # Calculate the radius of the sphere based on the max extent of the point cloud
                # / 1000 is a scaling factor to adjust a reasonable value size of the sphere
                radius = self.max_extent * self.picked_point_highlight_size / 1000
                self.draw_sphere(position, radius)

    def resizeGL(self, w, h):
        """
        Handle the resizing of the OpenGL viewport.

        This method is called whenever the widget is resized. It updates the OpenGL viewport to match the new widget
        dimensions and adjusts the projection matrix to maintain the correct aspect ratio.

        Args:
            w (int): The new width of the widget.
            h (int): The new height of the widget.
        """

        if h == 0:
            h = 1
        aspect = w / h
        glViewport(0, 0, w, h)

        # Update stored viewport
        self.viewport = np.array([0, 0, w, h], dtype=np.int32)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.fov * self.zoom_factor, aspect, max(self.near_plane, 0.1), self.far_plane)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def mousePressEvent(self, event):
        """
        Handle mouse press events for interaction with the point cloud.

        This method processes mouse press events to initiate interactions such as rotation, panning, and point
        selection. Depending on the mouse button and modifier keys pressed, the method determines the type of
        interaction (e.g., rotating, panning, or selecting points).

        Args:
            event (QMouseEvent): The mouse event containing details such as the button pressed and the mouse position.
        """

        self.last_mouse_pos = event.pos()
        modifiers = event.modifiers()

        if modifiers & Qt.ShiftModifier:
            if event.button() == Qt.LeftButton:
                # Shift + Left Click: Select a point
                self.pick_point(event.pos(), select=True)
            elif event.button() == Qt.RightButton:
                # Shift + Right Click: Deselect a point
                self.pick_point(event.pos(), select=False)
        elif modifiers & Qt.ControlModifier:
            if event.button() == Qt.LeftButton:
                # Ctrl + Left Click: Rotate around Z-axis
                self.setCursor(Qt.OpenHandCursor)
                self.is_rotating_z = True
            elif event.button() == Qt.RightButton or event.button() == Qt.MiddleButton:
                # Ctrl + Right/Middle Click: Pan along Z-axis
                self.setCursor(Qt.ClosedHandCursor)
                self.is_panning_z = True

            self.show_axis = True  # Show axis when panning
        else:
            if event.button() == Qt.LeftButton:
                # Rotate around X and Y axes
                self.setCursor(Qt.OpenHandCursor)
                self.is_rotating = True
            elif event.button() == Qt.RightButton or event.button() == Qt.MiddleButton:
                # Pan along X and Y axes
                self.setCursor(Qt.ClosedHandCursor)
                self.is_panning = True

            self.show_axis = True  # Show axis when panning

    def mouseDoubleClickEvent(self, event):
        """
        Handle mouse double-click events for updating the centre of rotation.

        This method processes double-click events to update the centre of rotation of the point cloud view. When the
        user double-clicks on a point, the centre of rotation is moved to that point, making it the new focal point
        for subsequent rotations.

        Args:
            event (QMouseEvent): The mouse event containing details such as the button pressed and the mouse position.
        """

        if event.button() == Qt.LeftButton:
            # Update the rotation center on double left-click
            self.update_rotation_center(event.pos())

    def mouseReleaseEvent(self, event):
        """
        Handle mouse release events for ending interactions.

        This method processes mouse release events to end interactions such as rotation or panning. When the user
        releases the mouse button, any ongoing rotation or panning is stopped, and the cursor is reset to its default
        state. The axis symbol is also hidden after the interaction ends.

        Args:
            event (QMouseEvent): The mouse event containing details such as the button released and the mouse position.
        """
        if event.button() == Qt.LeftButton:
            self.is_rotating = False
            self.is_rotating_z = False
            self.setCursor(Qt.ArrowCursor)
        elif event.button() == Qt.RightButton or event.button() == Qt.MiddleButton:
            self.is_panning = False
            self.is_panning_z = False
            self.setCursor(Qt.ArrowCursor)

        self.show_axis = False  # Hide axis when panning stops
        self.update()

    def mouseMoveEvent(self, event):
        """
        Handle mouse move events for updating the interaction state.

        This method processes mouse movement events to update the state of ongoing interactions such as rotation and
        panning. Depending on the interaction mode (e.g., rotating or panning), it adjusts the rotation angles or
        panning offsets based on the mouse movement distance.

        Args:
            event (QMouseEvent): The mouse event containing details such as the current mouse position.
        """

        if self.last_mouse_pos is None:
            return

        dx = event.x() - self.last_mouse_pos.x()
        dy = event.y() - self.last_mouse_pos.y()

        if self.is_rotating:
            # Rotate around X and Y axes
            # / 10 is a scaling factor to adjust the rotation sensitivity
            self.rot_x += dy * self.rotate_sensitivity / 10
            self.rot_y += dx * self.rotate_sensitivity / 10
        elif self.is_rotating_z:
            # Rotate around Z-axis
            self.rot_z += dx * self.rotate_sensitivity / 10  # Horizontal movement affects Z rotation
        elif self.is_panning:
            # Pan along X and Y axes
            # / 10000 is a scaling factor to adjust the panning sensitivity
            self.pan_x += dx * self.pan_sensitivity / 10000 * self.camera_distance
            self.pan_y -= dy * self.pan_sensitivity / 10000 * self.camera_distance
        elif self.is_panning_z:
            # Pan along Z-axis
            self.pan_z += dy * self.pan_sensitivity / 10000 * self.camera_distance  # Vertical movement affects Z panning

        self.last_mouse_pos = event.pos()
        self.update()

    def wheelEvent(self, event):
        """
        Handle mouse wheel events for zooming the view.

        This method processes mouse wheel events to adjust the zoom factor of the camera. The zoom sensitivity is
        controlled by the `zoom_sensitivity` attribute, and the resulting zoom factor is clamped between the
        `zoom_min_factor` and `zoom_max_factor` attributes to prevent excessive zooming in or out.

        Args:
            event (QWheelEvent): The wheel event containing details such as the direction and magnitude of the scroll.
        """

        delta = event.angleDelta().y()
        # / 1000 is a scaling factor to be able to set the defult_zoom_sensitivity to a reasonable value
        #
        zoom_step = delta * self.zoom_sensitivity / 1000
        self.zoom_factor *= (1 + zoom_step)
        self.zoom_factor = max(self.zoom_min_factor, min(self.zoom_factor, self.zoom_max_factor))  # Limit zoom factor

        # Show the axis symbol after zooming
        self.show_axis = True

        # Set a timer to hide the axis symbol after zooming is done
        self.axis_timer = QTimer(self)
        self.axis_timer.setSingleShot(True)
        self.axis_timer.timeout.connect(self.hide_axis_after_zoom)
        self.axis_timer.start(500)  # 500 milliseconds delay to hide the axis symbol

        self.update()

    def hide_axis_after_zoom(self):
        """Hide the axis symbol after zooming is completed."""
        self.show_axis = False
        self.update()

    def closeEvent(self, event):
        """
        Handle the close event for cleaning up resources.

        This method is called when the widget is about to be closed. It unbinds and deletes the vertex buffer object
        (VBO) if it exists, ensuring that all allocated resources are properly released before the widget is closed.

        Args:
            event (QCloseEvent): The close event containing details about the widget being closed.
        """

        # Make the OpenGL context current
        self.makeCurrent()

        if self.vbo is not None:
            self.vbo.unbind()
            self.vbo.delete()
            self.vbo = None  # Remove the reference to the VBO

        # Now, delete OpenGL resources explicitly
        self.deleteOpenGLResources()

        # Call the parent class's closeEvent
        super().closeEvent(event)

    def keyPressEvent(self, event):
        """
        Handle key press events for interaction with the point cloud.

        This method processes key press events to allow specific actions, such as deselecting all picked points. If
        the Escape key is pressed, a confirmation dialog is displayed, and if confirmed, all selected points are
        deselected.

        Args:
            event (QKeyEvent): The key event containing details such as the key pressed.
        """

        if event.key() == Qt.Key_Escape:
            # Create a confirmation dialog box
            reply = QMessageBox.question(self, 'Confirmation', 'Deselect all selected points?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                # Clear all selected points if confirmed
                self.picked_points_indices.clear()
                self.update()
        elif event.modifiers() & Qt.ControlModifier and event.key() == Qt.Key_R:
            self.reset_view()

        # Ensure the parent class handles other key events
        super(PCDViewerWidget, self).keyPressEvent(event)

    def pick_point(self, mouse_pos, select=True):
        """
        Handle point picking or deselecting points in the point cloud.

        This method is used to pick or deselect points in the point cloud based on a mouse click position. It uses
        OpenGL to project the clicked point onto the screen space and determines whether a point in the point cloud
        is close enough to be picked or deselected. If `select` is True, the method attempts to pick a point;
        otherwise, it attempts to deselect a point.

        Args:
            mouse_pos (QPoint): The position of the mouse click in widget coordinates.
            select (bool, optional): A flag indicating whether to select (True) or deselect (False) the point. Defaults
                to True.
        """

        if select:
            self.select_point_at(mouse_pos)
        else:
            self.deselect_point_at(mouse_pos)

    def project_to_screen(self, point_3d):
        """
        Project a 3D point onto the screen space.

        This method takes a 3D point in the world coordinate system and projects it onto the 2D screen space using the
        current model-view matrix, projection matrix, and viewport settings. The resulting screen coordinates can be
        used for tasks such as selecting or highlighting points in the point cloud.

        Args:
            point_3d (numpy.ndarray): A 3-element array representing the (x, y, z) coordinates of the point to be
                projected.

        Returns:
            numpy.ndarray: A 3-element array representing the (x, y, z) coordinates of the projected point in screen
            space.
        """

        # Ensure OpenGL context is current
        self.makeCurrent()

        # Use stored matrices
        modelview = self.model_view_matrix
        projection = self.projection_matrix
        viewport = self.viewport

        # Use gluProject to project the point
        screen_pos = gluProject(
            point_3d[0], point_3d[1], point_3d[2],
            modelview, projection, viewport
        )
        return np.array(screen_pos)

    def draw_sphere(self, position, radius, slices=16, stacks=16):
        """
        Draw a sphere at the specified position.

        This method uses OpenGL to render a sphere at the given 3D position in the point cloud space. The sphere
        is often used to highlight specific points, such as those that have been picked by the user. The appearance
        of the sphere can be customised using the radius, slices, and stacks parameters.

        Args:
            position (tuple or list or numpy.ndarray): A 3-element array representing the (x, y, z) coordinates of
                the sphere's centre.
            radius (float): The radius of the sphere to be drawn.
            slices (int, optional): The number of subdivisions around the Z-axis (similar to lines of longitude).
                Defaults to 16.
            stacks (int, optional): The number of subdivisions along the Z-axis (similar to lines of latitude).
                Defaults to 16.
        """

        glPushMatrix()
        glTranslatef(position[0], position[1], position[2])
        quadric = gluNewQuadric()
        gluQuadricDrawStyle(quadric, GLU_FILL)  # Use GLU_LINE for wireframe
        gluSphere(quadric, radius, slices, stacks)
        gluDeleteQuadric(quadric)
        glPopMatrix()

    def select_point_at(self, mouse_pos):
        """
        Select a point in the point cloud at the given mouse position.

        This method is used to select a point in the point cloud based on the mouse click position in widget coordinates.
        It reads the depth buffer to get the depth value at the mouse position and then unprojects the screen coordinates
        to world coordinates. The closest point to the unprojected coordinates is selected if it lies within a specified
        threshold.

        The distance threshold used for selecting points is defined by the `picking_point_threshold_factor` attribute.
        You can adjust this attribute to control how close a point must be to be considered selectable.

        If a point is successfully selected, its index is added to the `picked_points_indices` attribute, which stores the
        indices of all currently selected points.

        Args:
            mouse_pos (QPoint): The position of the mouse click in widget coordinates.
        """

        # Ensure OpenGL context is current
        self.makeCurrent()

        # Use stored matrices
        modelview = self.model_view_matrix
        projection = self.projection_matrix
        viewport = self.viewport

        # Get the window coordinates
        win_x = mouse_pos.x()
        win_y = viewport[3] - mouse_pos.y()  # Invert Y coordinate

        # Read the depth value at the mouse position
        z_buffer = glReadPixels(int(win_x), int(win_y), 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)
        win_z = z_buffer[0][0]

        # Handle cases where the depth value is 1.0 (background)
        if win_z == 1.0:
            return

        # Unproject the window coordinates to get the world coordinates
        world_coords = gluUnProject(win_x, win_y, win_z, modelview, projection, viewport)
        pick_point = np.array(world_coords[:3])

        # Find the closest point in the point cloud to the picked point
        distances = np.linalg.norm(self.points[:, :3] - pick_point, axis=1)
        min_distance_index = np.argmin(distances)
        min_distance = distances[min_distance_index]

        # Set a threshold to determine if a point is close enough to be considered picked
        threshold = self.max_extent * self.picking_point_threshold_factor

        if min_distance < threshold:
            # Add the index to the list of picked points
            if min_distance_index not in self.picked_points_indices:
                self.picked_points_indices.append(min_distance_index)

    def deselect_point_at(self, mouse_pos):
        """
        Deselect a point in the point cloud at the given mouse position.

        This method is used to deselect a previously selected point in the point cloud based on the mouse click position
        in widget coordinates. It projects the picked points to screen space and determines the closest point to the
        mouse click position. If the closest point lies within a specified pixel threshold, it is deselected.

        The pixel threshold used for deselecting points is defined by the `pixel_threshold` attribute. You can adjust
        this attribute to control how close a point must be to be considered for deselection.

        If a point is successfully deselected, its index is removed from the `picked_points_indices` attribute, which
        stores the indices of all currently selected points.

        Args:
            mouse_pos (QPoint): The position of the mouse click in widget coordinates.
        """

        # Ensure OpenGL context is current
        self.makeCurrent()

        # Use stored matrices
        viewport = self.viewport

        # Convert mouse position to screen space coordinates
        click_x = mouse_pos.x()
        click_y = viewport[3] - mouse_pos.y()  # Invert Y coordinate (adjust if necessary)

        # Project picked points to screen space
        screen_positions = []
        for index in self.picked_points_indices:
            point_3d = self.points[index, :3]
            screen_pos = self.project_to_screen(point_3d)
            screen_positions.append((index, screen_pos))

        # Find the closest picked point to the mouse click
        min_distance = float('inf')
        closest_index = None
        for index, screen_pos in screen_positions:
            dx = screen_pos[0] - click_x
            dy = screen_pos[1] - click_y
            distance = np.hypot(dx, dy)
            if distance < min_distance:
                min_distance = distance
                closest_index = index

        # Define a threshold in pixels (e.g., radius of the sphere in screen space)
        # TODO: Not sure if the pixel threshold is appropriate for all cases
        pixel_threshold = self.pixel_threshold

        if min_distance <= pixel_threshold:
            # Remove the point from picked points
            self.picked_points_indices.remove(closest_index)

    def update_rotation_center(self, mouse_pos):
        """
        Update the centre of rotation based on the given mouse position.

        This method is used to update the centre of rotation of the point cloud view based on a double-click event
        at a specific mouse position. It reads the depth value at the mouse position, unprojects the screen coordinates
        to world coordinates, and sets the centre of rotation to the closest point in the point cloud if it lies within
        a specified threshold.

        Args:
            mouse_pos (QPoint): The position of the mouse click in widget coordinates.
        """

        # Ensure OpenGL context is current
        self.makeCurrent()

        # Use stored matrices
        modelview = self.model_view_matrix
        projection = self.projection_matrix
        viewport = self.viewport

        # Get the window coordinates
        win_x = mouse_pos.x()
        win_y = viewport[3] - mouse_pos.y()  # Invert Y coordinate

        # Read the depth value at the mouse position
        z_buffer = glReadPixels(int(win_x), int(win_y), 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)
        win_z = z_buffer[0][0]

        # Handle cases where the depth value is 1.0 (background)
        if win_z == 1.0:
            # No depth information; do not update center
            return

        # Unproject the window coordinates to get the world coordinates
        world_coords = gluUnProject(win_x, win_y, win_z, modelview, projection, viewport)
        click_point = np.array(world_coords[:3])

        # Find the closest point in the point cloud to the click point
        distances = np.linalg.norm(self.points[:, :3] - click_point, axis=1)
        min_distance_index = np.argmin(distances)
        min_distance = distances[min_distance_index]

        # Set a threshold to determine if a point is close enough
        threshold = self.max_extent * self.picking_point_threshold_factor  # Adjust as needed

        if min_distance < threshold:
            # Update the center to the new point
            old_center = self.center.copy()
            self.center = self.points[min_distance_index, :3]

    def reset_view(self):
        """
        Reset the camera to its default position and orientation.

        This method restores the default settings for the camera, including zoom, rotation, and panning,
        allowing the user to return to the initial view of the point cloud.
        Specifically, the following attributes are reset:

        - `zoom_factor`: Set to `default_zoom_factor` to restore the original zoom level.
        - `rot_x`, `rot_y`, `rot_z`: Rotation angles around the X, Y, and Z axes are reset to default values, default_rot_x, etc.
        - `pan_x`, `pan_y`, `pan_z`: Panning offsets along the X, Y, and Z axes are reset to default values, default_pan_x.
        - `camera_distance`: Set to `default_camera_distance` to restore the original distance from the point cloud.

        After resetting these parameters, the view is updated to reflect the changes.
        """

        self.zoom_factor = self.default_zoom_factor
        self.rot_x = self.default_rot_x
        self.rot_y = self.default_rot_y
        self.rot_z = self.default_rot_z
        self.pan_x = self.default_pan_x
        self.pan_y = self.default_pan_y
        self.pan_z = self.default_pan_z
        self.camera_distance = self.default_camera_distance

        self.center[0] = -self.default_pan_x
        self.center[1] = -self.default_pan_y
        self.center[2] = -self.default_pan_z

        self.update()
