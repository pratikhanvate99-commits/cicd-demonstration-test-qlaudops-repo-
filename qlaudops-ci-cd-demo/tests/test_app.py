import json
import threading
import unittest
from urllib.request import urlopen

from app import create_server


class DashboardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = create_server(host="127.0.0.1", port=0)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def test_homepage_returns_dashboard(self):
        with urlopen(self.base_url + "/") as response:
            body = response.read().decode("utf-8")
            self.assertEqual(response.status, 200)
            self.assertIn("QlaudOps", body)
            self.assertIn("CloudOps Command Center", body)
            self.assertIn("Deployment pipeline", body)

    def test_health_endpoint_is_healthy(self):
        with urlopen(self.base_url + "/health") as response:
            payload = json.loads(response.read())
            self.assertEqual(response.status, 200)
            self.assertEqual(payload, {"status": "healthy", "service": "qlaudops-cloudops-dashboard"})

    def test_services_api_returns_four_services(self):
        with urlopen(self.base_url + "/api/services") as response:
            services = json.loads(response.read())
            self.assertEqual(response.status, 200)
            self.assertEqual(len(services), 4)
            self.assertTrue(any(item["status"] == "Warning" for item in services))
            self.assertTrue(all({"name", "status", "region", "uptime"}.issubset(item) for item in services))

    def test_dashboard_includes_cost_and_backup_sections(self):
        with urlopen(self.base_url + "/") as response:
            body = response.read().decode("utf-8")
            self.assertIn("Cloud cost breakdown", body)
            self.assertIn("Backup success rate", body)
            self.assertIn("Demo data for CI/CD showcase", body)


if __name__ == "__main__":
    unittest.main()
