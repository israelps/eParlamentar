from flask import Flask, render_template
from models import db
from models import User

app = Flask(__name__)
app.config.from_pyfile('config.py', silent=True)
app.jinja_env.line_statement_prefix = '##'
db.init_app(app)


@app.route('/')
@app.route('/<name>')
def hello(name=None):
    return render_template('index.html', name=name)


@app.route('/usuario')
def usuario():
    return render_template('usuario.html', usuarios=User.query.all())

if __name__ == '__main__':
    app.run()
