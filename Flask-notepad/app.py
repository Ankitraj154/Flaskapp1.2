from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired
import os

app = Flask(__name__)
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'default_user')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'default_password')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'default_db')

mysql = MySQL(app)

class NoteForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Add Note')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/notes', methods=['GET', 'POST'])
def notes():
    form = NoteForm()
    if form.validate_on_submit():
        content = form.content.data
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO notes (content) VALUES (%s)", [content])
        mysql.connection.commit()
        cur.close()
        flash('Note added successfully!', 'success')
        return redirect(url_for('notes'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM notes")
    notes = cur.fetchall()
    cur.close()
    
    return render_template('notes.html', form=form, notes=notes)

@app.route('/delete/<int:note_id>')
def delete(note_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM notes WHERE id = %s", [note_id])
    mysql.connection.commit()
    cur.close()
    flash('Note deleted successfully!', 'success')
    return redirect(url_for('notes'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
