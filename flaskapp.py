import locale
from flask import Flask, render_template, redirect
from models import Despesa
from models import Deputado
from models import db

locale.setlocale( locale.LC_ALL, 'pt_BR.UTF-8' )

app = Flask(__name__)
app.config.from_pyfile('config.py', silent=True)

# app.jinja_env.line_statement_prefix = '##'
db.init_app(app)


@app.route('/')
def hello():
    return render_template('layout.html')


@app.route('/deputados')
def deputados():
    deputados = Deputado.query.all()
    return render_template('deputados.html', deputados=deputados)


@app.route('/deputados/<int:ideCadastro>')
def deputado(ideCadastro):
    deputado = Deputado.query.get(ideCadastro)
    despesas = deputado.despesas
    total = 0
    valores = {'jan': 0, 'fev': 0, 'mar': 0, 'mai': 0, 'abr': 0, 'jun': 0, 'jul': 0, 'ago': 0, 'set': 0, 'out': 0,
               'nov': 0, 'dez': 0}

    for despesa in despesas:
        total += despesa.valor
        if despesa.mes == 1:
            valores['jan'] += despesa.valor
        if despesa.mes == 2:
            valores['fev'] += despesa.valor
        if despesa.mes == 3:
            valores['mar'] += despesa.valor
        if despesa.mes == 4:
            valores['abr'] += despesa.valor
        if despesa.mes == 5:
            valores['mai'] += despesa.valor
        if despesa.mes == 6:
            valores['jun'] += despesa.valor
        if despesa.mes == 7:
            valores['jul'] += despesa.valor
        if despesa.mes == 8:
            valores['ago'] += despesa.valor
        if despesa.mes == 9:
            valores['set'] += despesa.valor
        if despesa.mes == 10:
            valores['out'] += despesa.valor
        if despesa.mes == 11:
            valores['nov'] += despesa.valor
        if despesa.mes == 12:
            valores['dez'] += despesa.valor

    return render_template('deputado.html', valores=valores, despesas=despesas, deputado=deputado,
                           total=locale.currency(total, grouping=True))


@app.route('/atualizaDatabase')
def atualiza_deputados():
    Deputado.atualiza_database()
    Despesa.atualiza_database()
    return redirect('/deputados')


if __name__ == '__main__':
    app.run()
