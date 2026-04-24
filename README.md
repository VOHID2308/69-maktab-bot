# 🏫 SmartSchool Bot

SmartSchool Bot is an all-in-one Telegram bot designed to digitize and automate school management processes.
It connects **admins, teachers, students, and parents** in a single system.

---

## 🚀 Features

### 👨‍💼 Admin Panel

* Full control over the system
* Manage students, classes, schedules, announcements
* View all users
* Add new classes

### 🧑‍🏫 Teacher Panel

* View daily lessons
* Add homework
* Create tests and exams
* Track student performance
* Take attendance

### 👨‍🎓 Student Panel

* View schedule, homework, and results
* Submit homework (images)
* Participate in quizzes
* Use AI helper

### 👨‍👩‍👧 Parent Panel

* Monitor child (attendance, grades, homework)
* Receive notifications

---

## 🔐 Authentication System

* Role-based login (Admin, Teacher, Student, Parent)
* Each role has a separate password
* Passwords stored in `.env`
* Prevents unauthorized access

---

## 🎥 Intro System

* After login, users receive a short tutorial video
* Explains how to use the bot

---

## 🧩 Modules

* AttendanceManager
* HomeworkManager
* TestManager
* ScheduleManager
* GradeManager
* NotificationManager
* AIHelper
* GameManager

---

## 🗂 Project Structure

smartschool-bot/
│
├── config/
│   └── settings.py
│
├── database/
│   └── db.py
│
├── handlers/
│   ├── start_handler.py
│   ├── admin_handler.py
│   ├── teacher_handler.py
│   ├── student_handler.py
│   └── parent_handler.py
│
├── keyboards/
│   ├── main_menu.py
│   ├── admin_keyboards.py
│   ├── teacher_keyboards.py
│   ├── student_keyboards.py
│   └── parent_keyboards.py
│
├── videos/
│
├── .env
├── main.py
└── README.md

---

## ⚙️ Installation

### 1. Clone repository

git clone https://github.com/yourusername/smartschool-bot.git
cd smartschool-bot

### 2. Create virtual environment

python -m venv venv
venv\Scripts\activate

### 3. Install dependencies

pip install -r requirements.txt

### 4. Setup `.env`

BOT_TOKEN=your_bot_token
ADMIN_ID=your_telegram_id

STUDENT_PASSWORD=1111
TEACHER_PASSWORD=2222
PARENT_PASSWORD=3333
ADMIN_PASSWORD=4444

DB_PATH=database/school.db

### 5. Run bot

python main.py

---

## 🧠 How It Works

1. User sends /start
2. Selects role
3. Enters password
4. Gets role-based menu
5. Uses system

---

## 🎮 Gamification

* Quiz system
* Weekly leaderboard
* Student motivation

---

## 🤖 AI Assistant

Students can ask questions like:

* What is Past Simple?
* What is 2D array?

Bot gives simple answers.

---

## 📈 Future Improvements

* Web dashboard
* Mobile app
* Payment system
* Analytics

---

## 👨‍💻 Author

Developed by Abduvohid
