import win32evtlog
import re
from log_utils import open_event_log, close_event_log

def scan_logs():
    # Scan the system log files for suspicious entries.
    hand = open_event_log()
    if not hand:
        return
    
    try:
        total = win32evtlog.GetNumberOfEventLogRecords(hand)
        print(f"Scanning {total} log entries...")
        flags = win32evtlog.ReadEventLog(hand, flags, 0)

        suspicious_keywords = ["error", "fail", "attack", "unauthorized", "flasher", "crack", "noob", "glock", "skiddie"]
        for event in events:
            description = ' '.join(filter(None, event.StringInserts or []))
            if any(re.search(keyword, description, re.IGNORECASE) for keyword in suspicious_keywords):
                print(f"Suspicious log file found: {description}")
    finally:
        close_event_log(hand)