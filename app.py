import time
from concurrent.futures import ThreadPoolExecutor
from send_email import *
from status import *
from constants import *


out_streak = {i: 0 for i in CLINICIAN_LIST}
incident_open = {i: False for i in CLINICIAN_LIST}

"""Implementing the main status checker that sends email updates according to requirements"""
def check_one(clinician_id):
    try:
        status = get_clinician_status(clinician_id)
        if status is True:
            print(f"[{clinician_id}] in zone")
            if incident_open[clinician_id]:
                out_streak[clinician_id] = 0
                incident_open[clinician_id] = False
                send_email(f"Clinician {clinician_id} has returned.", f"Clinician {clinician_id} has returned to the safe zone")

        elif status is False:
            print(f"[{clinician_id}]  OUT of zone")
            out_streak[clinician_id] += 1
            if not incident_open[clinician_id] and out_streak[clinician_id] >=  NOISE_BOUND:
                print(f"EMAIL --> [{clinician_id}] in zone")
                incident_open[clinician_id] = True
                send_email("Out of Zone Alert.", f"Clinician {clinician_id} is out of zone")

        else:
            print(f"{clinician_id}] has no data")
            send_email("No Data from Api", f"We are unable to process location data for this clinician {clinician_id}")
    except Exception as e:
        print(f"[{clinician_id}] error: {e}")


"""Implementing Parallel threading for status checks per clinician_id"""
def poll_once(ids):
    with ThreadPoolExecutor(max_workers=len(ids)) as ex:
        ex.map(check_one, ids)


"""Implementing the summary updates  mailing"""
def formal_summary():
    body = "Summary Update for clinicians"
    message = ""
    for clinician_id in CLINICIAN_LIST:
        if incident_open[clinician_id]:
            message += f"[Clinician {clinician_id}] is out of zone\n"
        else:
            message += f"[Clinician {clinician_id}] is in zone\n"

    send_email(body, message)
    return


"""Implementing the monitoring loop that runs for an hour"""
def scheduler_loop(run_seconds=3600):
    print(f"Starting monitoring every {POLL_INTERVAL}s for {run_seconds} seconds")
    end_time = time.monotonic() + run_seconds
    next_summary = time.monotonic() + SUMMARY_INTERVAL

    while time.monotonic() < end_time:
        if time.monotonic() >= next_summary:
            formal_summary()
            next_summary = time.monotonic() + SUMMARY_INTERVAL

        start = time.monotonic()
        poll_once(CLINICIAN_LIST)
        elapsed = time.monotonic() - start
        time.sleep(max(0.0, float(POLL_INTERVAL) - elapsed))

scheduler_loop(run_seconds=3600)