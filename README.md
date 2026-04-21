# 📊 Attendify 2.0

A simple cloud-based attendance system

Attendify is a full-stack web app built to make attendance easier to manage. Instead of calling out names or maintaining registers, teachers can mark attendance quickly, and students can see their records instantly.

---

## 🚩 Why this exists

In most classrooms, attendance still works like this:

* Teachers spend ~10 minutes calling names
* Students give proxies
* Records aren’t always reliable

It’s slow, repetitive, and honestly a bit outdated.

---

## 💡 What Attendify does

* Lets teachers mark attendance in a few clicks
* Stores everything online (no registers)
* Shows students their attendance in real time
* Keeps things transparent with timestamps

---

## ✨ Features

* **Different roles** → Admin, Teacher, Student
* **Quick marking** → whole class in seconds
* **Live stats** → attendance %, total vs attended
* **Cloud storage** → MongoDB Atlas
* **Works on phone + desktop**

---

## 🏗️ How it works

This is a basic client-server setup:

* **Frontend** → HTML, CSS, JS
* **Backend** → Flask (Python)
* **Database** → MongoDB Atlas

Attendance is stored in a flexible format (NoSQL), which makes it easy to map students, subjects, and records.

---

## 🔐 Security stuff

* Flask sessions for login/auth
* Role-based access (students can’t access teacher/admin routes)
* Sensitive data stored using environment variables

---

## 🚀 Deployment

* Hosted on Render
* Auto-deploy using GitHub (CI/CD)

---

## 🛠️ Tech Stack

* HTML, CSS, JavaScript
* Python + Flask
* MongoDB Atlas
* Gunicorn
* Render

---

## 📂 Project Structure

```
Attendify/
├── app.py
├── requirements.txt
├── static/
│   ├── style.css
│   └── script.js
├── templates/
│   ├── login.html
│   ├── teacher.html
│   ├── admin.html
│   └── student.html
└── README.md
```

---

## ⚙️ How to run locally

Clone the repo:

```bash
git clone https://github.com/PYNE-ANKUR/Attendify.git
cd Attendify
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Set your MongoDB URI:

```bash
export MONGO_URI="your_connection_string"
```

Run the app:

```bash
python app.py
```

---

## 🌐 Live link

[https://attendify-2-0-p2kj.onrender.com](https://attendify-2-0-p2kj.onrender.com)

---

## 🔮 Things to add later

* Face recognition attendance
* Bluetooth/device-based validation
* Better analytics dashboard

---

## 👨‍💻 Built by

Ankur
Samridhi Kulshrestha

* more **resume-ready (with impact statements)**
* or more **casual/devlog style (like “what we struggled with”)**
