import pygame

import numpy as np

import inputHandling as inputHandling
import json
import math

# ----------------------------------------
# Initialise the simulation
# ----------------------------------------


class Rendering:
    """Rendering class. Handles the rendering of the simulation. Stores all rendering related variables and functions.

    Parameters
    ----------
    screen : Pygame.Surface
        The screen on which this Rendering class should render
    args : Namespace
        The arguments passed to the program
    """

    with open("./graphics_engine/render_consts.json") as f:
        consts = json.load(f)

    def __init__(self, screen, args: object):
        self.screen = screen

        self.resolution = args.resolution
        self.render_mode = args.render_mode
        self.show_overlay = args.overlay
        self.fps = args.fps

        self.camera = {
            "position": np.array([-3.42, 8.2, -5.96], dtype=float),
            "rotation": np.array([0, 0, 0], dtype=float),
            "fov": 90,
            "farClip": 100,
            "nearClip": 0.01,
        }

        self.projection_matrix = self.getProjectionMatrix()

    def draw(self, simulation):
        """Draws the simulation, overlay, and grid on the screen using the provided simulation class

        Parameters
        ----------
        simulation : Simulation
            The simulation to draw
        """

        # Clear the screen
        self.screen.fill(self.consts["color_bg"])

        # Draw the points
        self.drawWorld(simulation)
        # Draw the overlay
        if (self.show_overlay):
            self.drawOverlay()

        # Apply changes to screen
        pygame.display.flip()

    def drawWorld(self, simulation):
        """Draws the world on the screen using the provided simulation class

        Parameters
        ----------
        simulation : Simulation
            The simulation to draw
        """

        # Math out this frame's camera rotation matrix
        camera_rotation_matrix = self.getCameraRotationMatrix()

        self.renderGameObjects(simulation, camera_rotation_matrix)
        self.renderFluids(simulation, camera_rotation_matrix)

    def renderFluids(self, simulation, camera_rotation_matrix):
        """Renders the fluids on the screen using the provided simulation class

        Parameters
        ----------
        simulation : Simulation
            The simulation to draw
        camera_rotation_matrix : numpy.ndarray
            The rotation matrix of the camera
        """

        for fluid in simulation.fluids:
            for p_position in fluid.p_positions:
                point_2D = self.vec3tovec2(p_position, camera_rotation_matrix)
                color = self.consts["color_fluid"]

                if point_2D == (-1, -1):
                    continue

                # Draw the point
                pygame.draw.circle(self.screen, color, point_2D, 3)

    def renderGameObjects(self, simulation, camera_rotation_matrix):
        """Renders the gameObjects on the screen using the provided simulation class

        Parameters
        ----------
        simulation : Simulation
            The simulation to draw
        camera_rotation_matrix : numpy.ndarray
            The rotation matrix of the camera
        """

        # Math out the 3d points on the canvas (1 unit away from the camera)

        if (self.render_mode == "points"):
            self.draw_as_points(simulation, camera_rotation_matrix)
        elif (self.render_mode == "wireframe"):
            self.draw_as_wires(simulation, camera_rotation_matrix)
        elif (self.render_mode == "solid"):
            self.draw_as_solids(simulation, camera_rotation_matrix)

    def draw_as_points(self, simulation, camera_rotation_matrix):
        """Draws the simulation as points on the screen using the provided simulation class

        Parameters
        ----------
        simulation : Simulation
            The simulation to draw
        camera_rotation_matrix : numpy.ndarray
            The rotation matrix of the camera
        """

        for object in simulation.gameObjects:
            for point in object.points:
                point_2D = self.vec3tovec2(point, camera_rotation_matrix)
                color = self.getColor(point)

                if point_2D == (-1, -1):
                    continue

                # Draw the point
                pygame.draw.circle(self.screen, color, point_2D, 3)

    def draw_as_solids(self, simulation, camera_rotation_matrix):
        """Draws the simulation as solids on the screen using the provided simulation class

        Parameters
        ----------
        simulation : Simulation
            The simulation to draw
        camera_rotation_matrix : numpy.ndarray
            The rotation matrix of the camera
        """

        # 12 colors
        colors = [
            (255, 0, 0),
            (255, 127, 0),
            (255, 255, 0),
            (127, 255, 0),
            (0, 255, 0),
            (0, 255, 127),
            (0, 255, 255),
            (0, 127, 255),
            (0, 0, 255),
            (127, 0, 255),
            (255, 0, 255),
            (255, 0, 127)
        ]
        for object in simulation.gameObjects:

            pre_baked_points = []
            pre_baked_colors = []

            for point in object.points:
                pre_baked_points.append(self.vec3tovec2(point, camera_rotation_matrix))
                # pre_baked_colors.append(self.getColor(point))

            for i, face in enumerate(object.faces):

                # Project the face's points
                face_2D = [
                    pre_baked_points[face[0] - 1],
                    pre_baked_points[face[1] - 1],
                    pre_baked_points[face[2] - 1],
                ]
                color = colors[i % 12]

                # If one of the points is behind the camera, don't render the face
                if face_2D[0] == (-1, -1) or face_2D[1] == (-1, -1) or face_2D[2] == (-1, -1):
                    continue

                # If the winding order is CCW, don't render the face
                abX = face_2D[1][0] - face_2D[0][0]
                abY = face_2D[1][1] - face_2D[0][1]
                acX = face_2D[2][0] - face_2D[0][0]
                acY = face_2D[2][1] - face_2D[0][1]

                if (abX * acY - abY * acX) < 0:
                    continue

                # Color gradient not implemented
                pygame.draw.polygon(self.screen, color, face_2D)

    def draw_as_wires(self, simulation, camera_rotation_matrix):
        """Draws the simulation as wireframes on the screen using the provided simulation class

        Parameters
        ----------
        simulation : Simulation
            The simulation to draw
        camera_rotation_matrix : numpy.ndarray 
            The rotation matrix of the camera
        """

        for object in simulation.gameObjects:
            pre_baked_points = []
            pre_baked_colors = []
            for point in object.points:
                pre_baked_points.append(self.vec3tovec2(point, camera_rotation_matrix))
                pre_baked_colors.append(self.getColor(point))

            for face in object.faces:

                if pre_baked_points[face[0] - 1] == (-1, -1) or pre_baked_points[face[1] - 1] == (-1, -1) or pre_baked_points[face[2] - 1] == (-1, -1):
                    continue

                face_2D = [
                    pre_baked_points[face[0] - 1],
                    pre_baked_points[face[1] - 1],
                    pre_baked_points[face[2] - 1]]
                colors = [
                    pre_baked_colors[face[0] - 1],
                    pre_baked_colors[face[1] - 1],
                    pre_baked_colors[face[2] - 1]
                ]

                pygame.draw.line(self.screen, colors[0], face_2D[0], face_2D[1], 1)
                pygame.draw.line(self.screen, colors[1], face_2D[1], face_2D[2], 1)
                pygame.draw.line(self.screen, colors[2], face_2D[2], face_2D[0], 1)

    # Main projection function: From world space to screen space
    def vec3tovec2(self, point, camera_rotation_matrix):
        """Converts a 3d point to a 2d point on the screen

        Parameters
        ----------
        point : numpy.ndarray
            The point to convert
        camera_rotation_matrix : numpy.ndarray
            The rotation matrix of the camera

        Returns
        -------
        tuple
            The 2d point on the screen
        """

        # To determine a point's position on the screen:
        # - Express the point's position in camera coordinates
        # - Apply the rotation of the camera
        # - Apply homogenous coordinates
        # - Normalize the 2d vector

        camera_position = self.camera["position"]

        # Apply change of origin and apply orientation
        point = np.matmul(camera_rotation_matrix, (point - camera_position))

        # Apply homogenous coordinates
        point = np.array([point[0], point[1], point[2], 1])

        # Apply projection matrix
        point = np.matmul(self.projection_matrix, point)

        # Remove points behind the camera
        if point[2] < 0:
            return (-1, -1)

        # Normalize the vector
        point /= point[3]

        # Remove points outside of NDC space
        if point[0] < -1 or point[0] > 1 or point[1] < -1 or point[1] > 1:
            return (-1, -1)

        # Apply viewport transformation
        point[0] = point[0] * self.resolution[0]/2
        point[1] = point[1] * self.resolution[1]/2

        # Apply offset
        screen_x = self.resolution[0]/2 + point[0]
        screen_y = self.resolution[1]/2 - point[1]

        return (screen_x, screen_y)

    def drawOverlay(self):
        """Draws the overlay on the screen
        """

        font = pygame.font.SysFont("Roboto", 30)

        overlay_w = self.consts["overlay_size"][0]/100 * self.resolution[0]
        overlay_h = self.consts["overlay_size"][1]/100 * self.resolution[1]

        hud = pygame.Surface((overlay_w, overlay_h), pygame.SRCALPHA)

        pygame.draw.rect(hud, self.consts["color_overlay_bg"],
                         (0, 0, overlay_w, overlay_h), 0, 10)
        pygame.draw.rect(hud, self.consts["color_overlay_border"],
                         (0, 0, overlay_w, overlay_h), 2, 10)

        # Overlay content
        text = []

        # Camera Position
        text.append(
            font.render(
                "Camera: " + str([round(num, 2) for num in self.camera["position"]]),
                True, self.consts["color_overlay_txt"]))
        # Camera Rotation
        text.append(font.render("Camera rotation: " + str([round(np.degrees(num), 2)
                    for num in self.camera["rotation"]]), True, self.consts["color_overlay_txt"]))
        # FOV
        text.append(font.render("FOV: " + str(round(self.camera["fov"], 2)),
                    True, self.consts["color_overlay_txt"]))

        for i in range(len(text)):
            rect = text[i].get_rect(
                centery=((i+1)*overlay_h/(len(text)+1)), left=10)
            hud.blit(text[i], rect)

        self.screen.blit(hud, (self.consts["overlay_pos"][0]/100 * self.resolution
                          [0], self.consts["overlay_pos"][1]/100 * self.resolution[1]))

    def drawGrid(self, camera_rotation_matrix):
        """Draws the grid on the screen

        Parameters
        ----------
        camera_rotation_matrix : numpy.ndarray
            The rotation matrix of the camera
        """

        x_limits = [-5, 5]
        z_limits = [-5, 5]

        # Draw the grid
        for i in range(x_limits[0], x_limits[1] + 1):
            point_s = [x_limits[0], 0, i]
            point_e = [x_limits[1], 0, i]
            coords_s = self.vec3tovec2(point_s, camera_rotation_matrix)
            coords_e = self.vec3tovec2(point_e, camera_rotation_matrix)
            color = (255, 255, 255)
            pygame.draw.line(self.screen, color, coords_s, coords_e, 1)

        for i in range(z_limits[0], z_limits[1] + 1):
            point_s = [i, 0, z_limits[0]]
            point_e = [i, 0, z_limits[1]]
            coords_s = self.vec3tovec2(point_s, camera_rotation_matrix)
            coords_e = self.vec3tovec2(point_e, camera_rotation_matrix)
            color = (255, 255, 255)
            pygame.draw.line(self.screen, color, coords_s, coords_e, 1)

    def updateVarsOnResize(self):
        """Updates the variables when the window is resized
        """

        self.resolution = pygame.display.get_surface().get_size()
        self.projection_matrix = self.getProjectionMatrix(self.camera, self.resolution)

    # Returns the projection matrix from current simVars (mostly run when window is resized and on init)

    def getProjectionMatrix(self):
        """Returns the projection matrix from current simVars (mostly run when window is resized and on init)

        Returns
        -------
        numpy.ndarray
            The projection matrix
        """

        # Create projection matrix
        nearClip = self.camera["nearClip"]
        farClip = self.camera["farClip"]
        fov = self.camera["fov"]
        aspect_ratio = self.resolution[0] / self.resolution[1]

        projection_matrix = np.array([
            [1/(aspect_ratio * math.tan(math.radians(fov)/2)), 0, 0, 0],
            [0, 1/(math.tan(math.radians(fov)/2)), 0, 0],
            [0, 0, (farClip + nearClip)/(farClip - nearClip),
             (-2 * farClip * nearClip)/(farClip - nearClip)],
            [0, 0, 1, 0]
        ])

        return projection_matrix

    # Retrieve color value from point

    def getColor(self, point):
        """Retrieves the color value from the point

        Parameters
        ----------
        point : numpy.ndarray
            The point to get the color from

        Returns
        -------
        tuple
            The color value
        """

        dst_to_origin = math.sqrt(
            point[0] * point[0] + point[1] * point[1] + point[2] * point[2])
        dst_to_origin = max(min(dst_to_origin, 5), 0)
        ratio = dst_to_origin/5
        r = 255 + ratio * (42 - 255)
        g = ratio * (85 - 0)
        b = ratio * (91 - 0)
        color = (r, g, b)

        # Deal with NaN error values (although shouldn't be doing that)
        if not color:
            color = (0, 255, 0)

        return (color)

    # Returns the rotation matrix from the camera's orientation

    def getCameraRotationMatrix(self):
        """Returns the rotation matrix from the camera's orientation

        Returns
        -------
        numpy.ndarray
            The rotation matrix
        """

        cos_x = math.cos(self.camera["rotation"][0])
        sin_x = math.sin(self.camera["rotation"][0])
        cos_y = math.cos(self.camera["rotation"][1])
        sin_y = math.sin(self.camera["rotation"][1])
        cos_z = math.cos(self.camera["rotation"][2])
        sin_z = math.sin(self.camera["rotation"][2])

        Rot_x = np.array([
            [1, 0, 0],
            [0, cos_x, -sin_x],
            [0, sin_x, cos_x]
        ])
        Rot_y = np.array([
            [cos_y, 0, sin_y],
            [0, 1, 0],
            [-sin_y, 0, cos_y]
        ])
        Rot_z = np.array([
            [cos_z, -sin_z, 0],
            [sin_z, cos_z, 0],
            [0, 0, 1]
        ])

        # Full matrix = Rot_x * Rot_y * Rot_z
        rotation_matrix = np.matmul(np.matmul(Rot_x, Rot_y), Rot_z)

        return (rotation_matrix)
