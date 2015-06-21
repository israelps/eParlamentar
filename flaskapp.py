from flask import Flask, render_template, redirect
from models import Despesa
from models import Deputado
from models import db

app = Flask(__name__)
app.config.from_pyfile('config.py', silent=True)
# app.jinja_env.line_statement_prefix = '##'
db.init_app(app)


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/deputados')
def deputados():
    deputados = Deputado.query.all()
    return render_template('deputados.html', deputados=deputados)


@app.route('/deputados/<int:ideCadastro>')
def deputado(ideCadastro):
    deputado = Deputado.query.filter_by(ideCadastro=ideCadastro).first()
    return render_template('deputado.html', deputado=deputado)


@app.route('/atualizaDeputados')
def atualiza_deputados():
    Deputado.atualiza_database()
    return redirect('/deputados')

@app.route('/atualizaDespesas')
def atualiza_despesas():
    Despesa.atualiza_database()
    return redirect('/deputados')

if __name__ == '__main__':
    app.run()
