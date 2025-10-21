import unittest
import os
from edge_worker import handle_edge_detection_task

class TestEdgeDetectionWorker(unittest.TestCase):

    def setUp(self):
        """
        Set up before each test, prepare necessary files.
        """
        if not os.path.exists("client_results"):
            os.mkdir("client_results")

        # Ensure a sample image exists in the "images" folder for edge detection.

    def test_edge_detection_processing(self):
        """
        Test the edge detection processing function.
        """
        task = {
            "client_id": "test_client_edge",
            "task_type": "edge_detect",
            "image_name": "cake.jpg"
        }

        # Run the edge detection worker
        result = handle_edge_detection_task(task)

        # Check if the result is as expected
        self.assertEqual(result["client_id"], "test_client_edge")
        self.assertTrue(result["status"].startswith("edge detection processed"))
        self.assertTrue(os.path.exists(result["output"]), f"Output file {result['output']} does not exist.")

    def tearDown(self):
        """
        Clean up after each test, remove files created for testing.
        """
        if os.path.exists("client_results"):
            for f in os.listdir("client_results"):
                os.remove(os.path.join("client_results", f))

if __name__ == '__main__':
    unittest.main()
