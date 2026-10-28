#!/usr/bin/env python3
from job_manager import JobManager
import time

def test_job_lifecycle():
    """Test complete job lifecycle."""
    manager = JobManager()
    
    # 1. Create a new job
    job_id = manager.create_job("data_processing_job")
    print(f"Created Job ID: {job_id}, Initial Status: pending")
    
    # 2. Start the job
    manager.start_job(job_id)
    
    # 3. Simulate work
    time.sleep(2)
    
    # 4. Complete job with sample results
    sample_results = {"records_processed": 1500, "errors": 0}
    manager.complete_job(job_id, sample_results)
    
    # 5. Retrieve final status
    status_info = manager.get_job_status(job_id)
    print(f"Final Job Status Details: {status_info}")
    
    # 6. Calculate duration
    duration = manager.get_job_duration(job_id)
    print(f"Job Execution Duration: {duration:.4f} seconds")
    
    manager.close()

def test_failed_job():
    """Test job failure scenario."""
    manager = JobManager()
    
    # 1. Create failing job
    job_id = manager.create_job("failing_job")
    
    # 2. Start job
    manager.start_job(job_id)
    time.sleep(1)
    
    # 3. Fail job
    manager.fail_job(job_id, "Connection timeout while connecting to downstream API.")
    
    # 4. Retrieve status
    status_info = manager.get_job_status(job_id)
    print(f"Failed Job Status Details: {status_info}")
    
    manager.close()

def test_query_by_status():
    """Test querying jobs by status."""
    manager = JobManager()
    
    completed_jobs = manager.get_jobs_by_status("completed")
    print(f"\nCompleted Jobs Count: {len(completed_jobs)}")
    for j in completed_jobs:
        print(f"  - ID: {j['job_id']}, Name: {j['job_name']}, Results: {j['result_data']}")
    
    failed_jobs = manager.get_jobs_by_status("failed")
    print(f"\nFailed Jobs Count: {len(failed_jobs)}")
    for j in failed_jobs:
        print(f"  - ID: {j['job_id']}, Name: {j['job_name']}, Error: {j['error_message']}")
    
    manager.close()

if __name__ == "__main__":
    print("=== Testing Job Lifecycle ===")
    test_job_lifecycle()
    
    print("\n=== Testing Failed Job ===")
    test_failed_job()
    
    print("\n=== Testing Query by Status ===")
    test_query_by_status()
