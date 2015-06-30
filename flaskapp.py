import locale

from flask import Flask, render_template, redirect
import os
from models import Despesa
from models import Deputado
from models import db

locale.setlocale(locale.LC_ALL, '')

app = Flask(__name__)
app.config.from_pyfile('config.py', silent=True)
if os.environ.get('OPENSHIFT_POSTGRESQL_DB_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('OPENSHIFT_POSTGRESQL_DB_URL')
else: app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/eparlamentar'
# app.jinja_env.line_statement_prefix = '##'
db.init_app(app)


@app.route('/')
def hello():
    despesa_pt = Despesa.query.filter_by(deputado_id=None)
    valor = 0

    for i in despesa_pt:
        valor+=i.valor
    return render_template('index.html',despesa_pt=despesa_pt, valor=locale.currency(valor, grouping=True))


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
    valores = {'jan':0,'fev':0,'mar':0,'mai':0,'abr':0,'jun':0,'jul':0,'ago':0,'set':0,'out':0,'nov':0,'dez':0}

    for despesa in despesas:
        total += despesa.valor
        if despesa.mes == 1:
            valores['jan']+= despesa.valor
        if despesa.mes == 2:
            valores['fev']+= despesa.valor
        if despesa.mes == 3:
            valores['mar']+= despesa.valor
        if despesa.mes == 4:
            valores['abr']+= despesa.valor
        if despesa.mes == 5:
            valores['mai']+= despesa.valor
        if despesa.mes == 6:
            valores['jun']+= despesa.valor
        if despesa.mes == 7:
            valores['jul']+= despesa.valor
        if despesa.mes == 8:
            valores['ago']+= despesa.valor
        if despesa.mes == 9:
            valores['set']+= despesa.valor
        if despesa.mes == 10:
            valores['out']+= despesa.valor
        if despesa.mes == 11:
            valores['nov']+= despesa.valor
        if despesa.mes == 12:
            valores['dez']+= despesa.valor



    return render_template('deputado.html', valores=valores,despesas=despesas, deputado=deputado, total=locale.currency(total, grouping=True))


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
