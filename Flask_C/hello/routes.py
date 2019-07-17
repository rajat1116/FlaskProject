# imports
from flask import render_template, url_for, flash, redirect, request, session, send_file
from hello import app
from hello.forms import RegistrationForm, LoginForm, CandidateForm, SearchForm, ProgessTrack
import pypyodbc
import secrets
import os
from passlib.hash import sha256_crypt

connection = pypyodbc.connect('Driver={SQL Server}; Server=LAPTOP-RUUC0E0L; Database=Users; trusted_connection=yes')

@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/search", methods=['GET', 'POST'])
def search():
    form = SearchForm()
    curs = connection.cursor()
    selec = ("SELECT job_id, candidatename, email, contact, notice, skill, source, cv "
             "FROM candidatedel ")
    curs.execute(selec)
    result = curs.fetchall()
    if request.method == 'POST':
        if form.selectN.data == '':
            form.selectN.data = '%'
            select = ("SELECT u.email, candidatename, contact, skill, notice, job_id, source  "
                      "FROM candidatedel as u INNER JOIN roundTable as t "
                      "ON u.email=t.email "
                      "WHERE skill like ? AND notice like ? AND job_id like ? AND " + form.selectR.data + " like ?")
            values = [form.selectS.data, form.selectN.data, form.selectJ.data, form.selectT.data]
            print(values)
            curs.execute(select, values)
            result = curs.fetchall()
            if result:
                flash("Filter Applied", 'success')
            else:
                flash("No Record Found", 'danger')
    return render_template('Search.html', form=form, result=result)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        if request.method == 'POST':
            result = request.form
            cursor1 = connection.cursor()
            insert = ("INSERT INTO details "
                      "(email, password, username) "
                      "VALUES(?,?,?)")
            
            values = list(result.values())
            print(sha256_crypt.encrypt(values[1]))
            values = [values[2], values[3], sha256_crypt.encrypt(values[1])]
            cursor1.execute(insert, values)
            connection.commit()
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            cu = connection.cursor()
            username_form = str(form.email.data)
            password_form = str(form.password.data)
            select = ("SELECT email,password "
                      "FROM details "
                      "WHERE email= ?")
            cu.execute(select, [username_form])
            results = cu.fetchone()
            print(results)
            if username_form and password_form in results:
                session['loggedin'] = True
                session['username'] = username_form
                flash('You have been logged in!', 'success')
                print(results)
                return redirect(url_for('Hrmenu'))
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/adminmenu", methods=['GET', 'POST'])
def adminMenu():
    return render_template('AdminMenu.html')

@app.route("/hrmenu", methods=['GET','POST'])
def Hrmenu():
    return render_template('hrmenu.html')


@app.route("/rounds", methods=['GET', 'POST'])
def RoundStat():
    cursor5 = connection.cursor()
    cursor5.execute("SELECT * FROM roundTable")
    result = cursor5.fetchall()
    connection.commit()
    return render_template('round.html', title='Round', data=result)


@app.route("/candidatetable", methods=['GET', 'POST'])
def candidatedetails():
    cursor4 = connection.cursor()
    cursor4.execute("SELECT job_id, candidatename, email, contact, notice, skill, source, cv FROM candidatedel")
    result = cursor4.fetchall()
    connection.commit()
    return render_template('candidateTable.html', title='Login', data=result)


@app.route('/download<email>')
def download(email):
    cus = connection.cursor()
    select = ("SELECT cv "
          "FROM candidatedel "
          "WHERE email= ?")
    cus.execute(select, [email])
    result = cus.fetchone()
    print(result)
    return send_file("static/profile_pics/" +result[0], attachment_filename=result[0])


@app.route("/adminlogin", methods=['GET', 'POST'])
def Adminlogin():
    form = LoginForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            cu = connection.cursor()
            username_form = str(form.email.data)
            password_form = str(form.password.data)
            select = ("SELECT email,password "
                      "FROM adminlogin "
                      "WHERE email= ?")
            cu.execute(select, [username_form])
            results = cu.fetchone()
            print(results)
            if username_form and password_form in results:
                # session['loggedin'] = True
                session['Adminloggedin'] = True
                session['username'] = username_form
                flash('You have been logged in!', 'success')
                print(results)
                return redirect(url_for('adminMenu'))
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('loginAdmin.html', title='Login', form=form)


@app.route('/logout')
def logout():
    if 'loggedin' in session:
        session.pop('loggedin', None)
        session.pop('username', None)
        return redirect(url_for('login'))

@app.route('/Adminlogout')
def Adminlogout():
    session.pop('Adminloggedin', None)
    session.pop('username', None)
    return redirect(url_for('home'))


def save_picture(file):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(file.filename)
    file_fn = random_hex + f_ext
    file_path = os.path.join(app.root_path, 'static/profile_pics', file_fn)
    file.save(file_path)
    return file_fn


@app.route('/candidateprofile', methods=['GET', 'POST'])
def candidateprofile():
    form = CandidateForm()
    flash(f'Candidate Profile created for {form.candidatename.data}!', 'success')
    if form.validate_on_submit():
        if form.cv.data:
            resume_file = save_picture(form.cv.data)
            session['photo'] = resume_file
            print(session['photo'])
            cursor3 = connection.cursor()
            print(form.cv.data)
            result = request.form
            insert = ("INSERT INTO candidatedel "
                      "(email, candidatename, contact, notice, skill, source, job_id, cv) "
                      "VALUES(?,?,?,?,?,?,?,?)")
            values = list(result.values())
            print(values)
            ind = [values[2], values[1], values[3], values[4], values[5], values[6], values[7], resume_file]
            cursor3.execute(insert, ind)
            connection.commit()
            flash('Your changes have been saved', 'success')
            return redirect(url_for('candidateprofile'))

    return render_template('candidate.html', title='Register', form=form)

@app.route('/track', methods=['GET', 'POST'])
def progresstrack():
    form = ProgessTrack()
    if form.validate_on_submit():
        candidate = form.selectC.data
        rounds = form.selectR.data
        status = form.selectS.data
        con = connection.cursor()

        select = ("SELECT email "
              "FROM candidatedel "
              "WHERE Candidatename= ?")
        con.execute(select, [candidate])
        result = con.fetchone()
        print(result)
        select = ("SELECT email "
                "FROM roundTable "
                "WHERE email= ?")
        con.execute(select, [result[0]])
        result1 = con.fetchone()
        print(result1)
        
        if not result1:
            insert1 = ("INSERT into roundTable "
                   "(email) "
                   "VALUES(?)")
            print(str(result[0]))
            con.execute(insert1, [str(result[0])])
            con.commit()
        
        insert2 = ("UPDATE roundTable "
               "SET " + rounds + "= ? "
                                    "WHERE email= ?")
        con.execute(insert2, [str(status), str(result[0])])
        con.commit()
        flash('Success', 'success')

    return render_template('roundProgress.html', title='Track', form=form)
