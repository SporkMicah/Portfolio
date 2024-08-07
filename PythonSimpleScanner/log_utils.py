import win32evtlog

def open_event_log(server='localhost', log_type='System'):
    #Open an event log and return its handle.
    try:
        return win32evtlog.OpenEventLog(server, log_type)
    except Exception as e:
        print(f"Failed to open event log: {e}")
        return None

def close_event_log(handle):
    #Close an event log handle
    if handle:
        win32evtlog.CloseEventLog(handle)