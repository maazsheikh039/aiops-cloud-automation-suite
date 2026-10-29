from app import create_app
from app.models import db, JobHistory
from datetime import datetime, timedelta
import random

def populate_sample_data():
    '''Create sample job history data for testing'''
    app = create_app()
    
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        job_names = ['backup-database', 'deploy-app', 'run-tests', 'cleanup-logs']
        statuses = ['success', 'failed', 'running']
        environments = ['dev', 'staging', 'prod']
        users = ['admin', 'devops', 'jenkins']
        
        for i in range(25):
            name = random.choice(job_names)
            status = random.choice(statuses)
            env = random.choice(environments)
            user = random.choice(users)
            
            start = datetime.utcnow() - timedelta(days=random.randint(0, 6), hours=random.randint(0, 23))
            end = None
            duration = None
            err = None
            
            if status != 'running':
                end = start + timedelta(seconds=random.randint(30, 600))
                duration = int((end - start).total_seconds())
                if status == 'failed':
                    err = "Simulated connection timeout or exit code 1"
                    
            job = JobHistory(
                job_name=name,
                status=status,
                start_time=start,
                end_time=end,
                duration=duration,
                user=user,
                environment=env,
                error_message=err
            )
            db.session.add(job)
            
        db.session.commit()
        print("Created 25 sample job history entries successfully!")

if __name__ == '__main__':
    populate_sample_data()
