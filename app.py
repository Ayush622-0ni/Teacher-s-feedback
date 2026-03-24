from flask import Flask, render_template, request
import psycopg2
import os

app = Flask(__name__)

# ================= DATABASE CONNECTION =================

DATABASE_URL = os.environ.get("DATABASE_URL") 

def get_connection():
    return psycopg2.connect(DATABASE_URL)

# ================= ROUTES =================

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/feedback', methods=['GET','POST'])
def feedback():
    return render_template('feedback.html')

@app.route('/submit', methods=['POST'])
def submit():
    te = request.form['teacher']
    su = request.form['subject']
    ra = request.form['rating']
    teaching = request.form['teaching_quality']
    communication = request.form['communication_skill']
    pu = request.form['punctuality']
    feed = request.form['feedback']

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO feedback_data 
        (teacher_name, subject, rating, teaching_quality,
         communication_skill, punctuality, feedback)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (te, su, ra, teaching, communication, pu, feed))

    conn.commit()
    cur.close()
    conn.close()

    return render_template('submit.html')

@app.route('/admin_portal')
def admin_portal():
    return render_template('admin_portal.html')

@app.route('/portal', methods=['GET','POST'])
def portal():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM feedback_data")
    data = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('portal.html', himan=data)

# ================= RUN =================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)