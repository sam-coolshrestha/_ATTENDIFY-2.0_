# _ATTENDIFY-2.0_

attendify-2-0-p2kj.onrender.com

Attendify 📊
A Cloud-Based Student Attendance Management System

Attendify is a full-stack web application designed to digitize and automate the attendance process. It eliminates the inefficiencies of manual record-keeping and provides real-time transparency for both educators and students.

🚩 The Problem Statement
Traditional attendance management in schools and colleges is flawed by two major issues:

Inefficiency: Teachers spend 10–15 minutes of every lecture manually calling out names. It is physically tiring, repetitive, and wastes valuable instructional time.

Proxy Attendance: Paper registers are easy to manipulate. Students often mark attendance for absent friends ("proxies"), leading to fraudulent records and a lack of accountability.

Attendify solves this by providing a digital checklist for teachers and a live dashboard for students, ensuring every entry is timestamped and instantly visible.

✨ Features
Role-Based Access: Specialized dashboards for Admins, Teachers, and Students.

Effortless Marking: Teachers can mark a whole class in seconds using a digital checklist.

Real-Time Analytics: Students view their attendance percentage and "Total vs. Attended" stats instantly.

Cloud Database: Powered by MongoDB Atlas for 24/7 availability and secure data storage.

Responsive UI: Accessible from both mobile devices (for teachers in class) and desktops.

🏗️ Technical Architecture & Working
The system follows a modern Client-Server Architecture:

Backend: Built with Python & Flask. It handles the business logic, session security, and data routing.

Database: MongoDB Atlas (NoSQL). We chose NoSQL for its flexible document structure, allowing us to store attendance records as JSON-like objects that map Student IDs to Subject IDs.

Security: The app uses Flask Sessions to ensure students cannot access admin/teacher routes. Sensitive credentials (like the database password) are hidden using Environment Variables.

Deployment: Hosted on Render with a CI/CD pipeline—every update pushed to GitHub is automatically deployed to the live site.

🛠️ Tech Stack
Frontend: HTML5, CSS3, JavaScript (Vanilla)

Backend: Python 3.x, Flask

Database: MongoDB Atlas

Production Server: Gunicorn

Hosting: Render

📂 Project Structure
Plaintext
Attendify/
├── app.py              # Main Flask server & API routes
├── requirements.txt    # Python dependencies (Flask, Pymongo, etc.)
├── static/             # Frontend assets
│   ├── style.css       # Custom UI styling
│   └── script.js       # Asynchronous API handling
├── templates/          # Jinja2 HTML templates
│   ├── login.html      # Centralized login portal
│   ├── teacher.html    # Attendance marking interface
│   └── ...             # Admin and Student dashboards
└── README.md           # System documentation
⚙️ Setup & Installation
Clone the Repo:

Bash
git clone https://github.com/PYNE-ANKUR/Attendify.git
cd Attendify
Install Requirements:

Bash
pip install -r requirements.txt
Configure Environment:
Set your MONGO_URI variable in your terminal or hosting dashboard:

Bash
export MONGO_URI="your_mongodb_atlas_connection_string"
Run Locally:

Bash
python app.py
👨‍💻 Author
Ankur and Samridhi
Software Developer & Computer Science Student
