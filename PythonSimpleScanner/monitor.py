import win32evtlog
import time
from log_utils import open_event_log, close_event_log

def monitor_logs():
    # Monitor the system logs and provide a CLI readout of entries
    hand = open_event_log()
    if not hand:
        return
    
    try:
        flags = win32evtlog.EVENTLOG_FORWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
        while True:
            events = win32evtlog.ReadEventLog(hand, flags, 0)
            if events:
                for event in events:
                    print(f"Time Generated: {event.TimeGenerated}")
                    print(f"Source: {event.SourceName}")
                    print(f"Event ID: {event.EventID}")
                    if event.StringInserts:
                        print(f"Description: {' '.join(event.StringInserts)}")
                    print('-' * 50)
            time.sleep(5) # Sleep for 5 seconds before checking for new logs
    finally:
        close_event_log(hand)