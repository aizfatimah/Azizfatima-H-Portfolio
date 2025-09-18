import unittest
from database import insert_product, get_all

class TestApp(unittest.TestCase):
    def test_insert_product(self):
        insert_product("Test Product", 1.23)
        products = get_all("products")
        self.assertTrue(any(p[1] == "Test Product" for p in products))

if __name__ == "__main__":
    unittest.main()
