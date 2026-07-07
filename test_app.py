import unittest
from unittest.mock import patch
import app

class InventoryApiTestCase(unittest.TestCase):

    def setUp(self):
        """Runs before every single test to ensure a clean slate."""
        app.app.config["TESTING"] = True
        self.client = app.app.test_client()
        # Wipe our in-memory list clean before each test runs
        app.inventory = []

    @patch("app.requests.get")
    def test_add_item_via_external_api(self, mock_get):
        """Test adding an item where data is pulled from OpenFoodFacts."""
        # 1. Setup the fake API response data
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "status": 1,
            "product": {
                "product_name": "Test Orange Juice",
                "categories": "Beverages, Juices",
            },
        }

        # 2. Make the POST request with ONLY a barcode
        payload = {"barcode": "123456"}
        response = self.client.post("/inventory", json=payload)

        # 3. Assertions (Verify the results match expectations)
        self.assertEqual(response.status_code, 201)

        data = response.get_json()
        self.assertEqual(data["barcode"], "123456")
        self.assertEqual(data["name"], "Test Orange Juice")
        self.assertEqual(data["category"], "Beverages")
        self.assertEqual(data["quantity"], 0)  # Default value check

    @patch("app.requests.get")
    def test_add_item_api_failure_fallback(self, mock_get):
        """Test that the app handles an external API crash gracefully."""
        # Force the mock internet tool to drop the connection
        mock_get.side_effect = Exception("Network Down")

        payload = {"barcode": "999999"}
        response = self.client.post("/inventory", json=payload)

        # App should still succeed by using default fallback values
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data["name"], "Unknown Product")
        self.assertEqual(data["category"], "General")

    def test_prevent_duplicate_barcodes(self):
        """Test that our any() validation block blocks duplicate items."""
        # Manually prepopulate the list with one item
        app.inventory.append(
            {
                "barcode": "5555",
                "name": "Existing Item",
                "category": "General",
                "quantity": 5,
                "price": 1.0,
            }
        )

        # Try to add an item using that exact same barcode
        payload = {"barcode": "5555"}
        response = self.client.post("/inventory", json=payload)

        self.assertEqual(response.status_code, 400)
        self.assertIn("already exists", response.get_json()["error"])

    def test_complete_crud_flow(self):
        """Test retrieving, editing, and deleting an item from the array."""
        # 1. Seed data directly into our list
        test_item = {
            "barcode": "7777",
            "name": "Apple",
            "category": "Fruit",
            "quantity": 10,
            "price": 0.50,
        }
        app.inventory.append(test_item)

        # 2. Test GET specific item
        res_get = self.client.get("/inventory/7777")
        self.assertEqual(res_get.status_code, 200)

        # 3. Test PUT (Edit quantity and price)
        edit_payload = {"quantity": 15, "price": 0.60}
        res_put = self.client.put("/inventory/7777", json=edit_payload)
        self.assertEqual(res_put.status_code, 200)
        self.assertEqual(res_put.get_json()["quantity"], 15)
        self.assertEqual(res_put.get_json()["price"], 0.60)

        # 4. Test DELETE item
        res_del = self.client.delete("/inventory/7777")
        self.assertEqual(res_del.status_code, 204)
        self.assertEqual(len(app.inventory), 0)


if __name__ == "__main__":
    unittest.main()