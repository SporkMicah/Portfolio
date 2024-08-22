Web Application Security Scanner - Documentation
Table of Contents
Introduction
Installation
Configuration
Modules Overview
Running the Scanner
Understanding the Report
Extending the Scanner
Troubleshooting
Contributing
License
Introduction
The Web Application Security Scanner is a Python-based tool designed to identify and report vulnerabilities in web applications, with a focus on the OWASP Top 10. This documentation provides detailed instructions on how to install, configure, and use the scanner, as well as guidelines for contributing to its development.

Installation
Follow the steps outlined in the README.md to install the necessary dependencies and set up the project.

Configuration
config/config.json
The configuration file allows you to specify the target URLs and scanner settings:

target_urls: A list of URLs to scan.
scanner_settings: Controls aspects such as maximum threads and timeout settings.
Example:

json
Copy code
{
    "target_urls": [
        "https://example.com",
        "https://testsite.com"
    ],
    "scanner_settings": {
        "max_threads": 5,
        "timeout": 30
    }
}
config/logging.conf
This file controls logging configurations, including log levels and output formats.

Modules Overview
Each vulnerability is handled by a specific module. Below is a brief description of each:

SQL Injection: Detects vulnerabilities that allow attackers to execute arbitrary SQL queries.
XSS: Identifies potential points where scripts can be injected into web pages.
Broken Access Control: Checks for improperly protected resources.
Security Misconfiguration: Detects insecure server and application configurations.
Outdated Components: Identifies the use of components with known vulnerabilities.
Auth Failures: Tests for weak authentication mechanisms.
Software and Data Integrity Failures: Detects untrusted data deserialization and similar issues.
Logging & Monitoring Failures: Ensures proper logging and monitoring are in place.
SSRF: Detects vulnerabilities that allow attackers to make unauthorized requests.
Cryptographic Failures: Tests for inadequate or missing encryption practices.
Running the Scanner
To run the scanner, use:

bash
Copy code
python src/main.py
This will initiate scans for all configured URLs and generate a report in the reports/ directory.

Understanding the Report
The report is generated in JSON format and includes details of each vulnerability detected, categorized by type. Future versions will include options for HTML and PDF output.

Example Report Structure:
json
Copy code
{
    "https://example.com": {
        "SQL Injection": {
            "payload": "Not Vulnerable"
        },
        "XSS": {
            "payload": "Vulnerable"
        },
        "Cryptographic Failures": {
            "HTTPS Usage": "Not Secure",
            "TLS Version": "TLSv1.2",
            "TLS Status": "Secure"
        }
    }
}
Extending the Scanner
The scanner's modular design makes it easy to extend. To add a new vulnerability check:

Create a New Module: Add a .py file in the src/ directory.
Implement the Logic: Follow the pattern of existing modules.
Integrate with main.py: Import your new module and include it in the scan process.
Troubleshooting
Common Issues
Dependency Errors: Ensure all required packages are installed via pip install -r requirements.txt.
Timeouts: Adjust the timeout setting in config.json if scans are timing out frequently.
Logs
Check the logs/ directory (if configured) for detailed logs that can help diagnose issues.