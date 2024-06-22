import unittest
from app import app, db
from models import Cupcake

class CupcakeTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test client and sample data."""
        self.client = app.test_client()
        app.config['TESTING'] = True
        db.drop_all()
        db.create_all()

        self.cupcake = Cupcake(flavor="chocolate", size="large", rating=5, image="https://tinyurl.com/demo-cupcake")
        db.session.add(self.cupcake)
        db.session.commit()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_cupcakes(self):
        """Test listing all cupcakes."""
        response = self.client.get("/api/cupcakes")
        self.assertEqual(response.status_code, 200)
        self.assertIn("chocolate", str(response.data))

    def test_get_cupcake(self):
        """Test getting a single cupcake."""
        response = self.client.get(f"/api/cupcakes/{self.cupcake.id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("chocolate", str(response.data))

    def test_create_cupcake(self):
        """Test creating a cupcake."""
        response = self.client.post("/api/cupcakes", json={
            "flavor": "strawberry",
            "size": "medium",
            "rating": 4,
            "image": "https://tinyurl.com/demo-cupcake3"
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("strawberry", str(response.data))

    def test_update_cupcake(self):
        """Test updating a cupcake."""
        response = self.client.patch(f"/api/cupcakes/{self.cupcake.id}", json={
            "flavor": "vanilla",
            "size": "small"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("vanilla", str(response.data))

    def test_delete_cupcake(self):
        """Test deleting a cupcake."""
        response = self.client.delete(f"/api/cupcakes/{self.cupcake.id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Deleted", str(response.data))

    def test_404_get_cupcake(self):
        """Test getting a non-existent cupcake returns 404."""
        response = self.client.get("/api/cupcakes/999")
        self.assertEqual(response.status_code, 404)

    def test_404_update_cupcake(self):
        """Test updating a non-existent cupcake returns 404."""
        response = self.client.patch("/api/cupcakes/999", json={
            "flavor": "vanilla",
            "size": "small"
        })
        self.assertEqual(response.status_code, 404)

    def test_404_delete_cupcake(self):
        """Test deleting a non-existent cupcake returns 404."""
        response = self.client.delete("/api/cupcakes/999")
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
