from flask import Flask, jsonify, request
import sqlite3
from datetime import datetime
import json

app = Flask(__name__)
DB_PATH = 'jobs.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/jobs', methods=['GET'])
def get_jobs():
    """Retrieve all jobs or filter by status"""
    status = request.args.get('status')
    conn = get_db_connection()
    
    if status:
        jobs = conn.execute('SELECT * FROM jobs WHERE status = ?', (status,)).fetchall()
    else:
        jobs = conn.execute('SELECT * FROM jobs').fetchall()
    
    conn.close()
    return jsonify([dict(job) for job in jobs])

@app.route('/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    """Retrieve a specific job by ID"""
    conn = get_db_connection()
    job = conn.execute('SELECT * FROM jobs WHERE id = ?', (job_id,)).fetchone()
    conn.close()
    
    if job is None:
        return jsonify({'error': 'Job not found'}), 404
    
    return jsonify(dict(job))

@app.route('/jobs/<int:job_id>/status', methods=['PUT'])
def update_job_status(job_id):
    """
    Update job status and optionally store results
    """
    data = request.get_json() or {}
    status = data.get('status')
    result = data.get('result')
    
    valid_statuses = ['pending', 'processing', 'completed', 'failed']
    if status not in valid_statuses:
        return jsonify({'error': f'Invalid status. Must be one of {valid_statuses}'}), 400
        
    conn = get_db_connection()
    job = conn.execute('SELECT * FROM jobs WHERE id = ?', (job_id,)).fetchone()
    if not job:
        conn.close()
        return jsonify({'error': 'Job not found'}), 404
        
    conn.execute(
        'UPDATE jobs SET status = ?, result = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
        (status, result, job_id)
    )
    conn.commit()
    
    updated_job = conn.execute('SELECT * FROM jobs WHERE id = ?', (job_id,)).fetchone()
    conn.close()
    
    return jsonify(dict(updated_job))

@app.route('/jobs', methods=['POST'])
def create_job():
    """
    Create a new job
    """
    data = request.get_json() or {}
    job_type = data.get('job_type')
    payload = data.get('payload')
    
    if not job_type:
        return jsonify({'error': 'job_type is required'}), 400
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO jobs (job_type, payload, status) VALUES (?, ?, ?)',
        (job_type, payload, 'pending')
    )
    conn.commit()
    job_id = cursor.lastrowid
    
    new_job = conn.execute('SELECT * FROM jobs WHERE id = ?', (job_id,)).fetchone()
    conn.close()
    
    return jsonify(dict(new_job)), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
