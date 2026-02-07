# 📚 Electronic Library System

An Electronic Library System built using **Django** that allows users to browse books, borrow and return them, and manage their profiles easily.

---

## 🚀 Features

### 👤 User Features
- User registration and login
- View available books
- View book details
- Borrow and return books
- View borrowed books
- Write reviews and ratings
- Profile management

### 🛠 Admin Features
- Manage books, authors, and categories
- Manage users and borrowing records
- View late returns
- Full control through Django Admin Panel

---

## 🧑‍💻 Technologies Used
- Python 3
- Django Framework
- SQLite Database
- HTML5 / CSS3
- Bootstrap 5

---

## 📂 Project Structure
electronic_library/
│── accounts/
│── library/
│── core/
│── templates/
│── static/
│── db.sqlite3
│── manage.py
---

## ▶️ How to Run the Project

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install django

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
Then open:
http://127.0.0.1:8000/

🔐 Admin Panel
http://127.0.0.1:8000/admin/


📌 Notes
Borrowed books are tracked per user

Late returns are automatically detected

Admin can manage all data easily

👨‍🎓 Author
Student Name Here

📄 License
This project is for educational purposes only.


---

## ✅ شو تسلّم بالضبط؟
سلّم **3 أشياء فقط** (غالبًا هذا المطلوب):

1. ✅ **رابط GitHub** (فيه المشروع + README)
2. ✅ **ملف Word** (اللي عطيتك)
3. ✅ **فيديو شرح قصير** (لو مطلوب)

---

لو بدك:
- أعدّل README حسب دكتورك  
- أرتّب فيديو السكربت  
- أتأكد 100% إن المشروع مطابق للملف  

احكي 👍 وأنا معك خطوة بخطوة 💪 ​:contentReference[oaicite:0]{index=0}​
