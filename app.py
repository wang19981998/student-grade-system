from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)
DATA_FILE = 'data/students.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"students": [], "grades": []}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/students', methods=['GET'])
def get_students():
    return jsonify(load_data()['students'])

@app.route('/api/students', methods=['POST'])
def add_student():
    data = load_data()
    student = request.json
    student['id'] = len(data['students']) + 1
    data['students'].append(student)
    save_data(data)
    return jsonify(student)

@app.route('/api/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = load_data()
    for s in data['students']:
        if s['id'] == student_id:
            s.update(request.json)
            break
    save_data(data)
    return jsonify({"success": True})

@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    data = load_data()
    data['students'] = [s for s in data['students'] if s['id'] != student_id]
    data['grades'] = [g for g in data['grades'] if g['student_id'] != student_id]
    save_data(data)
    return jsonify({"success": True})

@app.route('/api/grades', methods=['GET'])
def get_grades():
    return jsonify(load_data()['grades'])

@app.route('/api/grades', methods=['POST'])
def add_grade():
    data = load_data()
    grade = request.json
    grade['id'] = len(data['grades']) + 1
    data['grades'].append(grade)
    save_data(data)
    return jsonify(grade)

@app.route('/api/grades/<int:grade_id>', methods=['PUT'])
def update_grade(grade_id):
    data = load_data()
    for g in data['grades']:
        if g['id'] == grade_id:
            g.update(request.json)
            break
    save_data(data)
    return jsonify({"success": True})

@app.route('/api/grades/<int:grade_id>', methods=['DELETE'])
def delete_grade(grade_id):
    data = load_data()
    data['grades'] = [g for g in data['grades'] if g['id'] != grade_id]
    save_data(data)
    return jsonify({"success": True})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    data = load_data()
    grades = data['grades']
    if not grades:
        return jsonify({"average": 0, "highest": 0, "lowest": 0, "total": 0})
    scores = [g['score'] for g in grades]
    return jsonify({
        "average": round(sum(scores) / len(scores), 2),
        "highest": max(scores),
        "lowest": min(scores),
        "total": len(scores)
    })

if __name__ == '__main__':
    os.makedirs('data', exist_ok=True)
    if not os.path.exists(DATA_FILE):
        save_data({"students": [], "grades": []})
    app.run(debug=True, host='0.0.0.0', port=5000)
