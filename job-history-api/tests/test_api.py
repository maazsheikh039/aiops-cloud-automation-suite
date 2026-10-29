import pytest
from app import create_app
from app.models import db, JobHistory
from app.config import TestConfig
from datetime import datetime

@pytest.fixture
def app():
    '''Create application for testing'''
    app = create_app(TestConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    '''Create test client'''
    return app.test_client()

@pytest.fixture
def sample_jobs(app):
    '''Create sample job data for tests'''
    with app.app_context():
        jobs = [
            JobHistory(
                job_name='backup-db',
                status='success',
                user='admin',
                environment='prod',
                start_time=datetime(2024, 1, 15, 10, 0),
                end_time=datetime(2024, 1, 15, 10, 5),
                duration=300
            ),
            JobHistory(
                job_name='deploy-app',
                status='failed',
                user='devops',
                environment='staging',
                start_time=datetime(2024, 1, 15, 11, 0),
                end_time=datetime(2024, 1, 15, 11, 2),
                duration=120,
                error_message='Connection timeout'
            ),
            JobHistory(
                job_name='run-tests',
                status='running',
                user='jenkins',
                environment='dev',
                start_time=datetime(2024, 1, 15, 12, 0)
            )
        ]
        for job in jobs:
            db.session.add(job)
        db.session.commit()
        return jobs

def test_create_job(client):
    '''Test creating a new job entry'''
    response = client.post('/jobs', json={
        "job_name": "new-integration-test",
        "status": "running",
        "user": "tester",
        "environment": "dev"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['job_name'] == 'new-integration-test'
    assert data['status'] == 'running'
    assert 'id' in data

def test_get_all_jobs(client, sample_jobs):
    '''Test retrieving all jobs'''
    response = client.get('/jobs')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 3

def test_get_job_by_id(client, sample_jobs):
    '''Test retrieving specific job by ID'''
    response = client.get('/jobs/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == 1
    assert data['job_name'] == 'backup-db'

def test_get_nonexistent_job(client):
    '''Test retrieving job that doesn't exist'''
    response = client.get('/jobs/999')
    assert response.status_code == 404

def test_update_job(client, sample_jobs):
    '''Test updating job status'''
    response = client.put('/jobs/3', json={
        "status": "success",
        "end_time": "2024-01-15T12:30:00"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert data['duration'] == 1800

def test_filter_by_status(client, sample_jobs):
    '''Test filtering jobs by status'''
    response = client.get('/jobs?status=success')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['status'] == 'success'

def test_filter_by_environment(client, sample_jobs):
    '''Test filtering jobs by environment'''
    response = client.get('/jobs?environment=prod')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['environment'] == 'prod'

def test_filter_by_user(client, sample_jobs):
    '''Test filtering jobs by user'''
    response = client.get('/jobs?user=admin')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['user'] == 'admin'

def test_filter_by_job_name(client, sample_jobs):
    '''Test filtering jobs by name'''
    response = client.get('/jobs?job_name=backup-db')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['job_name'] == 'backup-db'

def test_multiple_filters(client, sample_jobs):
    '''Test combining multiple filters'''
    response = client.get('/jobs?status=failed&environment=staging')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['job_name'] == 'deploy-app'

def test_get_statistics(client, sample_jobs):
    '''Test job statistics endpoint'''
    response = client.get('/jobs/stats')
    assert response.status_code == 200
    data = response.get_json()
    assert 'by_status' in data
    assert 'by_environment' in data
    assert data['by_status']['success'] == 1
    assert data['by_environment']['prod'] == 1
