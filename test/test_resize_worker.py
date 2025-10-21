import unittest
import os
from resize_worker import handle_resize_task

class TestResizeWorker(unittest.TestCase):

    def setUp(self):
        """
        Set up before each test, prepare necessary files.
        """
        if not os.path.exists("client_results"):
            os.mkdir("client_results")
        
        # Ensure a sample image exists in the "images" folder for resizing.
        # This can be an actual image or a mock image you generate for testing.

    def test_resize_processing(self):
        """
        Test the resizing processing function.
        """
        task = {
            "client_id": "test_client_resize",
            "task_type": "resize",
            "image_name": "cake.jpg",
            "resize_dimensions": [50, 50]
        }

        # Run the resize worker
        result = handle_resize_task(task)

        # Check if the result is as expected
        self.assertEqual(result["client_id"], "test_client_resize")
        self.assertTrue(result["status"].startswith("resize processed"))
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
