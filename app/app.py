from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)

bootstrap = Bootstrap(app)

@app.route('/')
def index():
      return render_template('index.html')

@app.route('/new-task')
def task():
      return render_template('new-task.html')

@app.errorhandler(404)
def page_not_found(e):
       return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
       return render_template('500.html'), 500

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)