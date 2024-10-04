import schedule
import time
from services.cron_netflow import process_netflow_data
from services.cron_syslog import process_syslog_data
from services.discover_eigrp import discover_network

def job_netflow():
    print("Running NetFlow data processing...")
    # process_netflow_data()

def job_syslog():
    print("Running Syslog data processing...")
    # process_syslog_data()

def job_eigrp_discovery():
    print("Running EIGRP network discovery...")
    # discover_network()

def run_cron_jobs():
    # Schedule the jobs at regular intervals
    schedule.every(10).minutes.do(job_netflow)  # Every 10 minutes
    schedule.every(5).minutes.do(job_syslog)    # Every 5 minutes
    schedule.every(15).minutes.do(job_eigrp_discovery)  # Every 15 minutes

    while True:
        # Run any pending jobs
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    print("Starting cron manager...")
    job_eigrp_discovery()
    job_netflow()
    job_syslog()
    run_cron_jobs()

