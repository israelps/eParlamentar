from flask import Flask, render_template
from models import db
from models import User

app = Flask(__name__)
app.config.from_pyfile('config.py', silent=True)
app.jinja_env.line_statement_prefix = '#'
db.init_app(app)


@app.route('/')
@app.route('/<name>')
def hello(name=None):
    return render_template('index.html', name=name)


@app.route('/usuario')
def usuario():
	u = User("Israel", "israelps@gmail.com")
	db.session.add(u)
	db.session.commit()
	return render_template('usuario.html', usuario=u)


if __name__ == '__main__':

    app.run()
