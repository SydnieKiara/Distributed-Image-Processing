import unittest
import os
from grayscale_worker import handle_grayscale_task

class TestGrayscaleWorker(unittest.TestCase):

    def setUp(self):
        """
        Set up before each test, prepare necessary files.
        """
        # Create a test directory for storing results
        if not os.path.exists("client_results"):
            os.mkdir("client_results")

        # Create a sample test image in the images directory
        # This would ideally be a known file to test against, e.g., a 1x1 pixel white image.
        # Here, we're assuming you have a "cake.jpg" image in the "images" folder.
        # If using mock images for testing, ensure you handle that in `setUp`.

    def test_grayscale_processing(self):
        """
        Test the grayscale processing function.
        """
        # Sample task to test grayscale worker
        task = {
            "client_id": "test_client",
            "task_type": "grayscale",
            "image_name": "cake.jpg"
        }

        # Run the grayscale worker
        result = handle_grayscale_task(task)

        # Check if the result is as expected
        self.assertEqual(result["client_id"], "test_client")
        self.assertTrue(result["status"].startswith("grayscale processed"))
        self.assertTrue(os.path.exists(result["output"]), f"Output file {result['output']} does not exist.")

    def tearDown(self):
        """
        Clean up after each test, remove files created for testing.
        """
        # Clean up any output files
        if os.path.exists("client_results"):
            for f in os.listdir("client_results"):
                os.remove(os.path.join("client_results", f))

if __name__ == '__main__':
    unittest.main()
