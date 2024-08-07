import argparse
from scanner import scan_logs
from monitor import monitor_logs

def main():
    parser = argparse.ArgumentParser(description='Windows System Log Monitoring System')
    parser.add_argument('mode', choices=['scan', 'monitor'], help='Mode to run the system in (scan or monitor)')
    args = parser.parse_args()

    if args.mode == 'scan':
        scan_logs()
    elif args.mode == 'monitor':
        monitor_logs()

if __name__ == "__main__":
    main()