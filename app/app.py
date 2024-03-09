from os import environ

from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '2YR44XT649dwNmhE'

bootstrap = Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app)

class Tasks(db.Model):
      __tablename__ = 'Tasks'
      id = db.Column(db.Integer, primary_key=True)
      task_name = db.Column(db.String(100), nullable=False)
      priority = db.Column(db.String(100), nullable=False)
      due_date = db.Column(db.DateTime(timezone=True))
      status = db.Column(db.String(100), nullable=False)

      def __repr__(self):
            return f'<Task> {self.task_name}'


class NewTask(FlaskForm):
      task_name = StringField('Task Name', validators=[DataRequired()])
      priority = SelectField('Priority', choices=[('Low'), ('Medium'), ('High'), ('Urgent')], validators=[DataRequired()])
      due_date = DateField('Due Date', format='%Y-%m-%d', validators=[DataRequired()])
      status = SelectField('Status', choices=[('Pending'), ('In Progress'), ('Blocked'), ('Completed')], validators=[DataRequired()])
      submit = SubmitField('Submit')

class EditTask(FlaskForm):
      task_name = StringField('Task Name', validators=[DataRequired()])
      priority = SelectField('Priority', choices=[('Low'), ('Medium'), ('High'), ('Urgent')], validators=[DataRequired()])
      due_date = DateField('Due Date', format='%Y-%m-%d', validators=[DataRequired()])
      status = SelectField('Status', choices=[('Pending'), ('In Progress'), ('Blocked'), ('Completed')], validators=[DataRequired()])
      submit = SubmitField('Submit')


@app.before_request
def init_db():
    with app.app_context():
        db.create_all()
        db.session.commit()

@app.route('/')
def index():
      tasks = Tasks.query.all()
      return render_template('index.html', tasks=tasks)

@app.route('/new-task', methods=['GET', 'POST'])
def task():
      form = NewTask()
      if form.validate_on_submit():
            task = Tasks(task_name=form.task_name.data,
                         priority=form.priority.data,
                         due_date=form.due_date.data,
                         status=form.status.data)
            db.session.add(task)
            db.session.commit()
            return redirect(url_for('.index'))
      return render_template('new-task.html', form=form)

@app.route('/edit-task', methods=['GET', 'POST'])
def edit_task():
      form = EditTask()
      return render_template('edit-task.html', form=form)

@app.errorhandler(404)
def page_not_found(e):
       return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
       return render_template('500.html'), 500

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)