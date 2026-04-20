from flask import Flask, render_template, request, jsonify, session
from pymongo import MongoClient
import random, time
import os

app = Flask(__name__)
app.secret_key = "secret123"

# ================= DB =================
MONGO_URI = os.environ.get("MONGO_URI") 
client = MongoClient(MONGO_URI)
db = client["attendify"]

# ================= HOME & LOGIN =================
@app.route('/')
def home(): return render_template("index.html")

@app.route('/login')
def login(): return render_template("login.html")

@app.route('/login-user', methods=['POST'])
def login_user():
    data = request.json
    user = db.users.find_one({"roll": data['roll'], "password": data['password']})
    if not user: return {"error": "Invalid login"}
    session['user'] = user['roll']
    session['role'] = user['role']
    return {"role": user['role']}

@app.route('/logout')
def logout():
    session.clear()
    return {"status": "logged out"}

# ================= ADMIN =================
@app.route('/admin')
def admin(): return render_template("admin.html")
@app.route('/add_student')
def add_student_page(): return render_template("add_student.html")
@app.route('/add_teacher')
def add_teacher_page(): return render_template("add_teacher.html")
@app.route('/add_subject')
def add_subject_page(): return render_template("add_subject.html")
@app.route('/assign')
def assign_page(): return render_template("assign.html")
@app.route('/admin_students')
def admin_students(): return render_template("admin_students.html")
@app.route('/admin_teachers')
def admin_teachers(): return render_template("admin_teachers.html")
@app.route('/admin_subjects')
def admin_subjects(): return render_template("admin_subjects.html")
@app.route('/admin_mapping')
def admin_mapping(): return render_template("admin_mapping.html")
@app.route('/admin_analytics')
def admin_analytics(): return render_template("admin_analytics.html") # NEW

# --- Admin APIs ---
@app.route('/add-student', methods=['POST'])
def add_student():
    db.users.insert_one({"roll": request.json['roll'], "password": request.json['password'], "role": "student", "deviceKey": None})
    return {"status": "Student added"}

@app.route('/add-teacher', methods=['POST'])
def add_teacher():
    db.users.insert_one({"roll": request.json['roll'], "password": request.json['password'], "role": "teacher"})
    return {"status": "Teacher added"}

@app.route('/add-subject', methods=['POST'])
def add_subject():
    db.subjects.insert_one({"name": request.json['name'], "teacher": None, "students": []})
    return {"status": "Subject added"}

@app.route('/assign-subject', methods=['POST'])
def assign_subject():
    db.subjects.update_one({"name": request.json['subject']}, {"$set": {"teacher": request.json['teacher']}})
    return {"status": "Teacher assigned"}

@app.route('/assign-student', methods=['POST'])
def assign_student():
    db.subjects.update_one({"name": request.json['subject']}, {"$addToSet": {"students": request.json['roll']}})
    return {"status": "Student assigned"}

@app.route('/get-students')
def get_students(): return jsonify(list(db.users.find({"role": "student"}, {"_id": 0})))
@app.route('/get-teachers')
def get_teachers(): return jsonify(list(db.users.find({"role": "teacher"}, {"_id": 0})))
@app.route('/get-subjects')
def get_subjects(): return jsonify(list(db.subjects.find({}, {"_id": 0})))
@app.route('/get-mapping')
def get_mapping():
    # Fetch all subjects and convert the cursor to a list
    mappings = list(db.subjects.find({}, {"_id": 0}))
    return jsonify(mappings)

@app.route('/admin/delete-subject', methods=['POST'])
def del_sub():
    s = request.json.get('name')
    db.attendance.delete_many({"subject": s})
    db.sessions.delete_many({"subject": s})
    db.subjects.delete_one({"name": s})
    return {"status": "Deleted"}

@app.route('/admin/delete-student', methods=['POST'])
def del_stu():
    r = request.json.get('roll')
    db.users.delete_one({"roll": r, "role": "student"})
    db.attendance.delete_many({"roll": r})
    db.subjects.update_many({}, {"$pull": {"students": r}})
    return {"status": "Deleted"}

@app.route('/admin/delete-teacher', methods=['POST'])
def del_tch():
    r = request.json.get('roll')
    db.users.delete_one({"roll": r, "role": "teacher"})
    db.subjects.update_many({"teacher": r}, {"$set": {"teacher": None}})
    return {"status": "Deleted"}

@app.route('/admin/change-password', methods=['POST'])
def chg_pwd():
    r = request.json.get('roll')
    p = request.json.get('password')
    db.users.update_one({"roll": r}, {"$set": {"password": p}})
    return {"status": "Updated"}

# NEW: Reset Device Key API
@app.route('/admin/reset-device', methods=['POST'])
def reset_device():
    r = request.json.get('roll')
    db.users.update_one({"roll": r}, {"$set": {"deviceKey": None}})
    return {"status": "Device key reset"}

# NEW: Analytics Data API
@app.route('/admin/analytics-data')
def analytics_data():
    subjects = list(db.subjects.find({}))
    labels, data = [], []
    for s in subjects:
        name = s["name"]
        tot_sessions = db.sessions.count_documents({"subject": name})
        num_students = len(s.get("students", []))
        
        if tot_sessions == 0 or num_students == 0: continue
        
        tot_possible = tot_sessions * num_students
        actual_att = db.attendance.count_documents({"subject": name})
        
        pct = (actual_att / tot_possible * 100)
        labels.append(name)
        data.append(round(pct, 2))
        
    return jsonify({"labels": labels, "data": data})

# ================= STUDENT =================
@app.route('/student')
def student(): return render_template("student_dashboard.html")
@app.route('/student_dashboard')
def student_dashboard(): return render_template("student_dashboard.html")
@app.route('/student_register')
def student_register(): return render_template("student_register.html")
# ================= STUDENT =================
@app.route('/student_attendance')
def student_attendance_page(): # Renamed the function to be unique
    # 1. Check if the teacher has already locked the portal
    locked_session = db.sessions.find_one({"active": True, "portalLocked": True})
    
    if locked_session:
        # If the teacher already revealed the code, new students can't enter
        return "<h1>Access Denied</h1><p>The attendance portal is locked. You must be in class on time.</p>"
    
    # 2. If not locked, show the page
    return render_template("student_attendance.html")
@app.route('/student_view')
def student_view(): return render_template("student_view.html")

@app.route('/save-device', methods=['POST'])
def save_device():
    data = request.json
    user_roll = data.get('roll')
    new_key = data.get('deviceKey')

    user = db.users.find_one({"roll": user_roll})
    if not user:
        return jsonify({"error": "User not found"}), 404

    # 1. Check if the user already has a device registered
    if user.get("deviceKey") is not None:
        return jsonify({"error": "Device already registered. Contact Admin to reset."}), 403

    # 2. Only allow registration if the current key is null
    db.users.update_one(
        {"roll": user_roll},
        {"$set": {"deviceKey": new_key}}
    )

    return jsonify({"status": "Device successfully registered!"})

@app.route('/mark-attendance', methods=['POST'])
def mark_attendance():
    data = request.json
    user = db.users.find_one({"roll": data['roll']})

    if not user: return {"error": "User not found"}
    if user['password'] != data['password']: return {"error": "Wrong password"}
    if user.get("deviceKey") != data['deviceKey']: return {"error": "Unauthorized device"}

    session_db = db.sessions.find_one({"subject": data['subject'], "code": data['code'], "active": True})
    if not session_db: return {"error": "Invalid session"}
    if time.time() - session_db['startTime'] > session_db['duration']: return {"error": "Session expired"}

    # Strict Duplicate Check
    if db.attendance.find_one({"roll": data['roll'], "sessionId": session_db['_id']}):
        return {"error": "Attendance already marked for this session!"}

    db.attendance.insert_one({
        "roll": data['roll'],
        "subject": data['subject'],
        "sessionId": session_db['_id'],
        "time": time.time()
    })
    return {"status": "Attendance marked"}

@app.route('/forfeit-attendance', methods=['POST'])
def forfeit_attendance():
    roll = request.json.get('roll')
    active_sessions = db.sessions.find({"active": True})
    active_ids = [s['_id'] for s in active_sessions]
    if active_ids:
        db.attendance.delete_many({"roll": roll, "sessionId": {"$in": active_ids}})
    return {"status": "Forfeited"}

@app.route('/student-percentage/<roll>')
def student_percentage(roll):
    subjs = list(db.subjects.find({"students": roll}))
    res = []
    for s in subjs:
        name = s["name"]
        tot = db.sessions.count_documents({"subject": name})
        att = db.attendance.count_documents({"roll": roll, "subject": name})
        pct = (att / tot * 100) if tot else 0
        res.append({"subject": name, "percentage": round(pct, 2)})
    return jsonify(res)

# ================= TEACHER =================
@app.route('/teacher')
def teacher(): return render_template("teacher_dashboard.html")
@app.route('/teacher_dashboard')
def teacher_dashboard(): return render_template("teacher_dashboard.html")
@app.route('/teacher_mark')
def teacher_mark(): return render_template("teacher_mark.html")
@app.route('/teacher_view')
def teacher_view(): return render_template("teacher_view.html")

@app.route('/my-subjects')
def my_subjects():
    if 'user' not in session or session.get("role") != "teacher": return jsonify([])
    return jsonify(list(db.subjects.find({"teacher": session['user']}, {"_id": 0})))

@app.route('/start-session', methods=['POST'])
def start_session():
    code = str(random.randint(1000, 9999))
    db.sessions.insert_one({
        "subject": request.json['subject'],
        "teacher": session.get("user"),
        "code": code,
        "startTime": time.time(),
        "duration": int(request.json['duration']),
        "active": True
    })
    return {"code": code}

@app.route('/live-attendance/<code>')
def live_attendance(code):
    session_db = db.sessions.find_one({"code": code})
    if not session_db: return jsonify({"count": 0, "students": []})
    attendees = list(db.attendance.find({"sessionId": session_db['_id']}))
    rolls = [s['roll'] for s in attendees]
    return jsonify({"count": len(rolls), "students": rolls, "active": session_db.get('active', True)})

@app.route('/end-session/<code>', methods=['POST'])
def end_session(code):
    db.sessions.update_one({"code": code}, {"$set": {"active": False}})
    return {"status": "Session ended"}

@app.route('/delete-session/<code>', methods=['POST'])
def delete_session(code):
    session_db = db.sessions.find_one({"code": code})
    if session_db:
        db.attendance.delete_many({"sessionId": session_db['_id']})
        db.sessions.delete_one({"code": code})
    return {"status": "Session deleted"}

@app.route('/all-absent/<code>', methods=['POST'])
def all_absent(code):
    session_db = db.sessions.find_one({"code": code})
    if session_db: db.attendance.delete_many({"sessionId": session_db['_id']})
    return {"status": "Everyone marked absent"}

@app.route('/attendance-percentage/<subject>')
def attendance_percentage(subject):
    subj = db.subjects.find_one({"name": subject})
    if not subj: return jsonify([])
    tot = db.sessions.count_documents({"subject": subject})
    if tot == 0: return jsonify([{"roll": r, "percentage": 0} for r in subj.get("students", [])])
    att = list(db.attendance.find({"subject": subject}))
    counts = {}
    for a in att: counts[a['roll']] = counts.get(a['roll'], 0) + 1
    res = []
    for r in subj.get("students", []):
        res.append({"roll": r, "percentage": round((counts.get(r, 0) / tot * 100), 2)})
    return jsonify(res)

# Update this route to handle the "Lockdown" state
@app.route('/reveal-code/<code>', methods=['POST'])
def reveal_code_api(code):
    # When code is revealed, we "lock" the session so no NEW students can join
    db.sessions.update_one({"code": code}, {"$set": {"portalLocked": True}})
    return {"status": "Portal locked, code revealed"}

# Update the student attendance page route to check for lockout


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)