from flask import Flask, render_template, request, redirect, jsonify

import sqlite3

app = Flask(__name__)

def init_db():

    conn = sqlite3.connect('career.db')

    c = conn.cursor()


    c.execute("DROP TABLE IF EXISTS students")
    c.execute('''CREATE TABLE students
      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
      name TEXT,
        email TEXT,
          phone TEXT,
            school TEXT, 
            marks INTEGER,
              interest TEXT,
                career TEXT)''')
    conn.commit();

    conn.close()

init_db()

@app.route('/')

def home(): return render_template('test.html')

@app.route('/predict', methods=['POST'])

def predict():

    name=request.form['name']; 

    email=request.form['email']; 

    phone=request.form['phone']; 

    school=request.form['school']; 

    marks=int(request.form['marks']);

    interest=request.form['interest']

    if marks>=90:
        career="Engineering / Doctor"

    elif marks>=75: 
        career="B.Sc / Management"

    elif "tech" in interest.lower():
        career="Software / IT"

    elif "art" in interest.lower(): 
        career="Designing / Arts"

    else: career="General Degree"

    conn=sqlite3.connect('career.db'); 

    c=conn.cursor()

    c.execute("INSERT INTO students (name,email,phone,school,marks,interest,career) VALUES (?,?,?,?,?,?,?)",(name,email,phone,school,marks,interest,career))

    conn.commit();

    conn.close()

    return render_template('result.html', name=name, email=email, phone=phone, school=school, marks=marks, interest=interest, career=career)

@app.route('/chatbot-api', methods=['POST'])

def chatbot_api():

    msg = request.json['message'].lower()

    if "tech" in msg or "computer" in msg:
        reply = "💻 Niku Tech ante istam kabatti Software Engineer / Data Scientist best!"

    elif "art" in msg or "design" in msg:
        reply = "🎨 Wow! Niku Arts ante Designing, Animation, UI/UX best career!"

    elif "doctor" in msg or "bio" in msg:
        reply = "🩺 Biology ante Doctor / Pharmacy try chey!"

    elif "marks" in msg: 
        reply = "📊 Marks ekkuva unte Engineering, takkuva unna kuda skills tho Software avvachu!"

    elif "hello" in msg or "hi" in msg:
        reply = "Hi Avanthi! 👋 Nenu FuturePath Bot. Nee interest cheppu, career cheptha!"

    else: 
        reply = "🤖 Nee interest enti? Tech, Arts, Science, Business ani cheppu!"
    return jsonify({"reply": reply})

@app.route('/admin-login', methods=['GET','POST'])

def admin_login():

    if request.method=='POST':

        if request.form['username']=='admin' and request.form['password']=='admin123': return redirect('/dashboard')

        else: return "Wrong Password"

    return render_template('admin_login.html')

@app.route('/dashboard')

def dashboard():

    conn=sqlite3.connect('career.db'); c=conn.cursor()

    c.execute("SELECT * FROM students ORDER BY id DESC");

    students=c.fetchall()

    c.execute("SELECT COUNT(*), AVG(marks) FROM students");

    row=c.fetchone()

    total=row[0] or 0; 
    avg=row[1] or 0

    c.execute("SELECT career, COUNT(*) FROM students GROUP BY career")

    career_data=c.fetchall();

    career_labels=[r[0] for r in career_data];

    career_counts=[r[1] for r in career_data]

    c.execute("SELECT name, marks FROM students ORDER BY id DESC LIMIT 5")

    marks_data=c.fetchall();

    marks_names=[r[0] for r in marks_data];

    marks_values=[r[1] for r in marks_data]

    conn.close()

    return render_template('dashboard.html', students=students, total=total, avg=round(avg,1), career_labels=career_labels, career_counts=career_counts, marks_names=marks_names, marks_values=marks_values)

@app.route('/delete-student/<id>')

def delete_student(id):

    conn=sqlite3.connect('career.db');

    c=conn.cursor(); 

    c.execute("DELETE FROM students WHERE id=?",(id,)); 

    conn.commit();

    conn.close()
    
    return redirect('/dashboard')

if __name__=='__main__': app.run(debug=True)