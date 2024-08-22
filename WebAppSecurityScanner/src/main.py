import json
import logging
import logging.config
from utils.report_generator import generate_report
from utils.vulnerability_scanner import VulnerabilityScanner
from injection_test import SQLInjectionTest
from xss_test import XSSTest
from access_control_test import AccessControlTest
from security_misconfig_test import SecurityMisconfigurationTest
from outdated_components_test import OutdatedComponentsTest
from auth_failures_test import AuthFailuresTest
from integrity_failures_test import IntegryFailuresTest
from logging_monitoring_test import LoggingMonitoringTest
from ssrf_test import SSRFTest

def load_config(config_file):
    with open(config_file, 'r') as file:
        return json.load(file)

def setup_logging(logging_config):
    logging.config.fileConfig(logging_config)

def main():
    config = load_config('config/config.json')
    setup_logging('config/logging.conf')

    scan_results = {}
    for url in config['target_urls']:
        logging.info(f"Starting scan for {url}")

        sql_injection_test = SQLInjectionTest(url)
        sql_result = sql_injection_test.run_test()

        xss_test = XSSTest(url)
        xss_result = xss_test.run_test()

        access_control_test = AccessControlTest(url)
        access_control_result = access_control_test.run_test()

        security_misconfig_test = SecurityMisconfigurationTest(url)
        security_misconfig_result = security_misconfig_test.run_test()

        outdated_components_test = OutdatedComponentsTest(url)
        outdated_components_result = outdated_components_test.run_test()

        auth_failures_test = AuthFailuresTest(url)
        auth_failures_result = auth_failures_test.run_test()

        integrity_failures_test = IntegryFailuresTest(url)
        integrity_failures_result = integrity_failures_test.run_test()

        logging_monitoring_test = LoggingMonitoringTest(url)
        logging_monitoring_result = logging_monitoring_test.run_test()

        ssrf_test = SSRFTest(url)
        ssrf_result = ssrf_test.run_test()

        scan_results[url] = {
            "SQL Injection": sql_result,
            "XSS": xss_result,
            "Broken Access Control": access_control_result,
            "Security Misconfiguration": security_misconfig_result,
            "Outdated Components": outdated_components_result,
            "Auth Failures": auth_failures_result,
            "Software and Data Integrity Failures": integrity_failures_result,
            "Logging and Monitoring Failures": logging_monitoring_result,
            "Server-Side Request Forgery (SSRF)": ssrf_result
        }

    # Generate a report 
    generate_report(scan_results, output_file='reports/scan_report_2024-08-22.json')

    logging.info("Scan completed successfully.")

if __name__ == "__main__":
    main()