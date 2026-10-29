from flask import Blueprint, request, jsonify
from app.models import db, JobHistory
from datetime import datetime

api = Blueprint('api', __name__)

@api.route('/jobs', methods=['POST'])
def create_job():
    data = request.get_json() or {}
    required_fields = ['job_name', 'status']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    job = JobHistory(
        job_name=data.get('job_name'),
        status=data.get('status'),
        user=data.get('user'),
        environment=data.get('environment'),
        error_message=data.get('error_message')
    )
    db.session.add(job)
    db.session.commit()
    return jsonify(job.to_dict()), 201

@api.route('/jobs', methods=['GET'])
def get_jobs():
    query = JobHistory.query
    
    status = request.args.get('status')
    if status:
        query = query.filter(JobHistory.status == status)
        
    job_name = request.args.get('job_name')
    if job_name:
        query = query.filter(JobHistory.job_name == job_name)
        
    environment = request.args.get('environment')
    if environment:
        query = query.filter(JobHistory.environment == environment)
        
    user = request.args.get('user')
    if user:
        query = query.filter(JobHistory.user == user)
        
    start_date = request.args.get('start_date')
    if start_date:
        try:
            dt = datetime.strptime(start_date, '%Y-%m-%d')
            query = query.filter(JobHistory.start_time >= dt)
        except ValueError:
            return jsonify({'error': 'Invalid start_date format. Use YYYY-MM-DD'}), 400
            
    end_date = request.args.get('end_date')
    if end_date:
        try:
            dt = datetime.strptime(end_date, '%Y-%m-%d')
            query = query.filter(JobHistory.start_time <= dt)
        except ValueError:
            return jsonify({'error': 'Invalid end_date format. Use YYYY-MM-DD'}), 400

    jobs = query.order_by(JobHistory.start_time.desc()).all()
    return jsonify([job.to_dict() for job in jobs]), 200

@api.route('/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    job = JobHistory.query.get_or_404(job_id)
    return jsonify(job.to_dict()), 200

@api.route('/jobs/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    job = JobHistory.query.get_or_404(job_id)
    data = request.get_json() or {}
    
    if 'status' in data:
        job.status = data['status']
    if 'error_message' in data:
        job.error_message = data['error_message']
    if 'end_time' in data:
        try:
            job.end_time = datetime.fromisoformat(data['end_time'])
            if job.start_time:
                delta = job.end_time - job.start_time
                job.duration = int(delta.total_seconds())
        except ValueError:
            return jsonify({'error': 'Invalid end_time ISO format'}), 400
            
    db.session.commit()
    return jsonify(job.to_dict()), 200

@api.route('/jobs/stats', methods=['GET'])
def get_stats():
    status_counts = db.session.query(JobHistory.status, db.func.count(JobHistory.id)).group_by(JobHistory.status).all()
    env_counts = db.session.query(JobHistory.environment, db.func.count(JobHistory.id)).group_by(JobHistory.environment).all()
    
    return jsonify({
        'by_status': {s[0] or 'unknown': s[1] for s in status_counts},
        'by_environment': {e[0] or 'unknown': e[1] for e in env_counts}
    }), 200
