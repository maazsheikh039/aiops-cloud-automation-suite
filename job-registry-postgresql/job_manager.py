import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("JobManager")

class JobManager:
    def __init__(self, host='localhost', database='job_registry', 
                 user='postgres', password='labpassword'):
        """Initialize database connection."""
        try:
            self.conn = psycopg2.connect(
                host=host,
                database=database,
                user=user,
                password=password
            )
            self.conn.autocommit = False
            logger.info("Successfully connected to PostgreSQL job_registry database.")
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise
    
    def create_job(self, job_name: str) -> int:
        """Create a new job entry with 'pending' status."""
        query = """
            INSERT INTO jobs (job_name, status, created_at)
            VALUES (%s, 'pending', CURRENT_TIMESTAMP)
            RETURNING job_id;
        """
        with self.conn.cursor() as cursor:
            cursor.execute(query, (job_name,))
            job_id = cursor.fetchone()[0]
            self.conn.commit()
            logger.info(f"Created job '{job_name}' with ID {job_id} [pending]")
            return job_id
    
    def start_job(self, job_id: int) -> bool:
        """Mark job as running and set started_at timestamp."""
        query = """
            UPDATE jobs
            SET status = 'running', started_at = CURRENT_TIMESTAMP
            WHERE job_id = %s;
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, (job_id,))
                self.conn.commit()
                logger.info(f"Job {job_id} started [running]")
                return True
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Failed to start job {job_id}: {e}")
            return False
    
    def complete_job(self, job_id: int, result_data: dict) -> bool:
        """Mark job as completed and store results."""
        query = """
            UPDATE jobs
            SET status = 'completed', 
                completed_at = CURRENT_TIMESTAMP, 
                result_data = %s
            WHERE job_id = %s;
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, (json.dumps(result_data), job_id))
                self.conn.commit()
                logger.info(f"Job {job_id} completed successfully [completed]")
                return True
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Failed to complete job {job_id}: {e}")
            return False
    
    def fail_job(self, job_id: int, error_message: str) -> bool:
        """Mark job as failed and store error message."""
        query = """
            UPDATE jobs
            SET status = 'failed', 
                completed_at = CURRENT_TIMESTAMP, 
                error_message = %s
            WHERE job_id = %s;
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, (error_message, job_id))
                self.conn.commit()
                logger.info(f"Job {job_id} failed: {error_message} [failed]")
                return True
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Failed to record failure for job {job_id}: {e}")
            return False
    
    def get_job_status(self, job_id: int) -> dict:
        """Retrieve current job status and metadata."""
        query = "SELECT * FROM jobs WHERE job_id = %s;"
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, (job_id,))
            result = cursor.fetchone()
            return dict(result) if result else None
    
    def get_jobs_by_status(self, status: str) -> list:
        """Retrieve all jobs with specified status."""
        query = "SELECT * FROM jobs WHERE status = %s ORDER BY job_id;"
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, (status,))
            return [dict(row) for row in cursor.fetchall()]
    
    def get_job_duration(self, job_id: int) -> float:
        """Calculate job execution duration in seconds."""
        query = """
            SELECT EXTRACT(EPOCH FROM (completed_at - started_at)) AS duration
            FROM jobs
            WHERE job_id = %s AND started_at IS NOT NULL AND completed_at IS NOT NULL;
        """
        with self.conn.cursor() as cursor:
            cursor.execute(query, (job_id,))
            row = cursor.fetchone()
            if row and row[0] is not None:
                return float(row[0])
        return None
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed.")
