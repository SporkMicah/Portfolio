import requests
import logging

class LoggingMonitoringTest:
    def __init__(self, url):
        self.url = url
        self.test_endpoints = [
           "/admin",
            "/login",
            "/error",
            "/logs" 
        ]

    def run_test(self):
        logging.info(f"Starting Logging and Monitoring Failures Test for {self.url}")
        results = {}
        for endpoint in self.test_endpoints:
            full_url = self.url + endpoint
            if self.is_logging_present(full_url):
                results[full_url] = "Logging detected (Could be a vulnerability)"
            else:
                results[full_url] = "No logging detected (Secure)"
        return results
    
    def is_logging_present(self, url):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200 and "log" in response.text.lower():
                return True
            return False
        except requests.RequestException as e:
            logging.error(f"Request error: {e}")
            return False