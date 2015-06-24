import locale
from flask import Flask, render_template, redirect
from models import Despesa
from models import Deputado
from models import db

locale.setlocale(locale.LC_ALL, '')

app = Flask(__name__)
app.config.from_pyfile('config.py', silent=True)
# app.jinja_env.line_statement_prefix = '##'
db.init_app(app)


@app.route('/')
def hello():
    despesa_pt = Despesa.query.filter_by(partido='PT',deputado_id=None)
    return render_template('index.html',despesa_pt=despesa_pt)


@app.route('/deputados')
def deputados():
    deputados = Deputado.query.all()
    return render_template('deputados.html', deputados=deputados)


@app.route('/despesas')
def despesas():
    total = 0
    despesas = Despesa.query.all()
    for despesa in despesas:
        total += despesa.valor
    media = total / 513
    return render_template('despesas.html', total=locale.currency(total, grouping=True),
                           media=locale.currency(media, grouping=True))


@app.route('/deputados/<int:ideCadastro>')
def deputado(ideCadastro):
    deputado = Deputado.query.get(ideCadastro)
    despesas = deputado.despesas
    total = 0
    for despesa in despesas:
        total += despesa.valor
    return render_template('deputado.html', despesas=despesas, deputado=deputado, total=locale.currency(total, grouping=True))


@app.route('/atualizaDeputados')
def atualiza_deputados():
    Deputado.atualiza_database()
    return redirect('/deputados')


@app.route('/atualizaDespesas')
def atualiza_despesas():
    Despesa.atualiza_database()
    return redirect('/deputados')

@app.route('/atualizaDatabase')
def atualiza_database():
    db.drop_all()
    db.create_all()
    return redirect('/')

if __name__ == '__main__':
    app.run()
