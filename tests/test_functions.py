import unittest
import numpy as np
import tempfile
import os
import json
import pygame
import sys

# Ensure parent directory is in search path for functions module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from functions import Point, Obj, Camera, load_json_obj, draw_impostor_sphere, render_scene

class TestFunctions(unittest.TestCase):
    def setUp(self):
        # Initialize pygame for rendering tests
        pygame.init()
        # Set up a hidden/dummy display mode or just create a Surface
        self.surface = pygame.Surface((400, 400))

    def test_point_initialization_and_properties(self):
        coords = np.array([1.0, 2.0, 3.0])
        p1 = Point(coords)
        self.assertTrue(np.array_equal(p1.Coordinates, coords))
        self.assertIsNone(p1.Radius)

        p2 = Point(coords, Radius=15.0)
        self.assertEqual(p2.Radius, 15.0)

    def test_point_transformations(self):
        p = Point(np.array([1.0, 0.0, 0.0]))
        
        # Test Scale
        p.Scale(2.0)
        self.assertTrue(np.array_equal(p.Coordinates, np.array([2.0, 0.0, 0.0])))
        
        # Test Translate
        p.Translate(np.array([1.0, 1.0, 1.0]))
        self.assertTrue(np.array_equal(p.Coordinates, np.array([3.0, 1.0, 1.0])))
        
        # Test Stretch
        p.Stretch(0, 2.0) # stretch X axis
        self.assertTrue(np.array_equal(p.Coordinates, np.array([6.0, 1.0, 1.0])))

    def test_point_rotation(self):
        # Rotate 90 degrees around Z axis (axis = 2)
        # (1, 0, 0) rotated 90 degrees around Z should become (0, 1, 0)
        p = Point(np.array([1.0, 0.0, 0.0]))
        p.Rotate(90, 2)
        # Using almost_equal due to float precision
        np.testing.assert_array_almost_equal(p.Coordinates, np.array([0.0, 1.0, 0.0]))

    def test_obj_edge_population(self):
        obj = Obj()
        obj.Points = [
            Point(np.array([0, 0, 0])),
            Point(np.array([1, 0, 0])),
            Point(np.array([0, 1, 0]))
        ]
        # Define a face (triangle)
        obj.Faces = [(0, 1, 2)]
        self.assertEqual(len(obj.Edges), 0)
        
        obj.Populate_Edges_From_Faces()
        # Edges should be: (0, 1), (1, 2), (0, 2) sorted
        self.assertEqual(len(obj.Edges), 3)
        self.assertIn((0, 1), obj.Edges)
        self.assertIn((1, 2), obj.Edges)
        self.assertIn((0, 2), obj.Edges)

    def test_obj_generation_methods(self):
        # Test single node generator
        obj = Obj().Generate_Single_Node(radius=50.0)
        self.assertEqual(len(obj.Points), 1)
        self.assertEqual(obj.Points[0].Radius, 50.0)
        self.assertEqual(obj.Points[0].Coordinates[0], 0.0)

        # Test grid generator
        obj_grid = Obj().Generate_Impostor_Grid(scale_factor=100, grid_size=3)
        self.assertEqual(len(obj_grid.Points), 27) # 3x3x3 grid
        for p in obj_grid.Points:
            self.assertEqual(p.Radius, 20.0)

        # Test unit sphere generator
        obj_sphere = Obj().Generate_Unit_Sphere(scale_factor=100, lat_count=6, lon_count=12)
        self.assertTrue(len(obj_sphere.Points) > 0)
        self.assertTrue(len(obj_sphere.Faces) > 0)

    def test_camera_and_projection(self):
        camera = Camera(np.array([0.0, 0.0, -10.0]))
        # Camera translates
        camera.Translate(np.array([1.0, 0.0, 0.0]))
        self.assertTrue(np.array_equal(camera.Coordinates, np.array([1.0, 0.0, -10.0])))
        
        # Test Projection
        obj = Obj()
        obj.Points = [Point(np.array([0.0, 0.0, 0.0]), Radius=10.0)]
        focal_length = 5
        
        # Relative point to camera is (0, 0, 0) - (1, 0, -10) = (-1, 0, 10)
        # Projection: X_proj = 5 * (-1) / 10 = -0.5
        # Y_proj = 5 * 0 / 10 = 0.0
        # Z_depth = 10.0
        projected = obj.Project_3D_To_2D(camera, focal_length)
        self.assertEqual(len(projected.Points), 1)
        np.testing.assert_array_almost_equal(projected.Points[0].Coordinates, np.array([-0.5, 0.0, 10.0]))
        self.assertEqual(projected.Points[0].Radius, 10.0)

    def test_load_json_obj(self):
        # Create a temporary json file representing a simple triangle
        data = {
            "points": [
                [0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0]
            ],
            "faces": [
                [0, 1, 2]
            ]
        }
        
        fd, path = tempfile.mkstemp(suffix=".json")
        try:
            with os.fdopen(fd, 'w') as tmp:
                json.dump(data, tmp)
                
            obj = load_json_obj(path, scale=1.0)
            self.assertEqual(len(obj.Points), 3)
            self.assertEqual(len(obj.Faces), 1)
            # load_json_obj automatically calls Populate_Edges_From_Faces
            self.assertEqual(len(obj.Edges), 3)
        finally:
            os.remove(path)

    def test_draw_impostor_sphere_execution(self):
        # Verify that draw_impostor_sphere runs without raising any exception
        try:
            draw_impostor_sphere(self.surface, (200, 200), 20.0, (255, 0, 0))
            draw_impostor_sphere(self.surface, (200, 200), 2.0, (255, 0, 0)) # Tiny radius path
            draw_impostor_sphere(self.surface, (200, 200), -5.0, (255, 0, 0)) # Negative path
        except Exception as e:
            self.fail(f"draw_impostor_sphere raised exception: {e}")

    def test_render_scene_execution(self):
        # Test rendering pipeline execution
        camera = Camera(np.array([0.0, 0.0, -100.0]))
        obj = Obj().Generate_Unit_Sphere(scale_factor=20, lat_count=4, lon_count=8)
        
        render_config = {
            "faces": True,
            "lines": True,
            "nodes": True,
            "node_style": "impostor",
            "default_node_radius": 5.0
        }
        theme = {
            "background": (0, 0, 0),
            "face": (255, 0, 0),
            "line": (0, 255, 0),
            "node": (0, 0, 255)
        }
        
        try:
            # 1. Test rendering list of objects
            render_scene(self.surface, 400, 400, camera, 100, [(obj, None)], render_config, theme)
            # 2. Test rendering single object directly
            render_scene(self.surface, 400, 400, camera, 100, obj, render_config, theme)
            # 3. Test rendering with wireframe only (faces disabled)
            render_config["faces"] = False
            render_scene(self.surface, 400, 400, camera, 100, obj, render_config, theme)
        except Exception as e:
            self.fail(f"render_scene raised exception: {e}")

if __name__ == '__main__':
    unittest.main()
