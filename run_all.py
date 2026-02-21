import time
import os
from s1_export import generate_tasks
from s2_submit import submit_batch
from s3_status import check_status
from s4_import import finalize_import

GOAL_TOTAL = 200
CHUNK_SIZE = 100      # Starting size
MIN_CHUNK_SIZE = 1000  # Size after failures
POLL_INTERVAL = 60 
MAX_FAILURES = 3       # max -failures before scaling down

def run_orchestrator():
    global CHUNK_SIZE
    total_processed = 0
    consecutive_failures = 0
    active_batches = {} # {job_id: "status"}

    print(f"Starting Dual-Batch Orchestrator (Initial Chunk: {CHUNK_SIZE})")

    while total_processed < GOAL_TOTAL or active_batches:
        
        if len(active_batches) < 2 and total_processed < GOAL_TOTAL:
            print(f"\nSlot available. Exporting {CHUNK_SIZE} rows...")
            
            if generate_tasks(limit=CHUNK_SIZE):
                job_id = submit_batch()
                
                if job_id:
                    active_batches[job_id] = "in_progress"
                    print(f"Submitted Batch {job_id}. Slots filled: {len(active_batches)}/2")
                    consecutive_failures = 0 # Reset failures on a successful submission
                else:
                    consecutive_failures += 1
                    print(f"Submission failed ({consecutive_failures}/{MAX_FAILURES})")
            else:
                print("No more data to export.")

        finished_jobs = []
        for job_id in list(active_batches.keys()):
            report = check_status(job_id)
            status = report['status']
            
            if status == 'completed':
                print(f"\nBatch {job_id} Finished! Importing...")
                count = finalize_import(report['output_file_id'])
                total_processed += count
                consecutive_failures = 0 # Reset on successful import
                print(f"Saved {count} rows. Session Total: {total_processed}")
                finished_jobs.append(job_id)
            
            elif status in ['failed', 'expired', 'cancelled']:
                consecutive_failures += 1
                print(f"\nBatch {job_id} {status}! (Failures: {consecutive_failures}/{MAX_FAILURES})")
                finished_jobs.append(job_id)
            
            else:
                # Progress display
                print(f"{job_id}: {status} ({report['completed']}/{report['total']})", end='\r')

        if consecutive_failures >= MAX_FAILURES:
            if CHUNK_SIZE > MIN_CHUNK_SIZE:
                print(f"\n{MAX_FAILURES} failures reached. Scaling down CHUNK_SIZE to {MIN_CHUNK_SIZE}...")
                CHUNK_SIZE = MIN_CHUNK_SIZE
                consecutive_failures = 0 # Reset counter to try with new size
            else:
                print("\nCritical Error: Failures continue even at minimum chunk size. Stopping.")
                return

        for job_id in finished_jobs:
            del active_batches[job_id]

        if active_batches:
            time.sleep(POLL_INTERVAL)
        else:
            if total_processed >= GOAL_TOTAL: break
            time.sleep(10)

    print(f"\nALL DONE. Total processed: {total_processed}")

if __name__ == "__main__":
    run_orchestrator()