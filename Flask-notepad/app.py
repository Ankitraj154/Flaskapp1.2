import os
import subprocess
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{os.environ.get('MYSQL_USER')}:{os.environ.get('MYSQL_PASSWORD')}@{os.environ.get('MYSQL_HOST')}/{os.environ.get('MYSQL_DB')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class NoteForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Add Note')

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/notes', methods=['GET', 'POST'])
def notes():
    form = NoteForm()
    if form.validate_on_submit():
        content = form.content.data
        note = Note(content=content)
        db.session.add(note)
        db.session.commit()
        flash('Note added successfully!', 'success')
        return redirect(url_for('notes'))

    notes = Note.query.all()
    return render_template('notes.html', form=form, notes=notes)

@app.route('/delete/<int:note_id>')
def delete(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    flash('Note deleted successfully!', 'success')
    return redirect(url_for('notes'))

def setup_database():
    with app.app_context():
        # Check if migrations exist
        migrations_exist = os.path.exists('migrations')
        if not migrations_exist:
            try:
                # Initialize database migration
                subprocess.run(['flask', 'db', 'init'], check=True)
            except Exception as e:
                print(f"Init error (probably already initialized): {e}")

        # Generate migration script
        subprocess.run(['flask', 'db', 'migrate'], check=True)

        # Apply migration to database
        subprocess.run(['flask', 'db', 'upgrade'], check=True)

if __name__ == '__main__':
    setup_database()
    app.run(host='0.0.0.0', port=5000, debug=True)
