from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = '2YR44XT649dwNmhE'

bootstrap = Bootstrap(app)

class NewTask(FlaskForm):
      task_name = StringField('Task Name', validators=[DataRequired()])
      priority = SelectField('Priority', choices=[(1, 'Low'), (2, 'Medium'), (3, 'High'), (4, 'Urgent')], validators=[DataRequired()])
      due_date = DateField('Due Date', format='%Y-%m-%d', validators=[DataRequired()])
      submit = SubmitField('Submit')

@app.route('/')
def index():
      return render_template('index.html')

@app.route('/new-task', methods=['GET', 'POST'])
def task():
      form = NewTask()
      return render_template('new-task.html', form=form)

@app.errorhandler(404)
def page_not_found(e):
       return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
       return render_template('500.html'), 500

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)