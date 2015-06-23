from flask.ext.sqlalchemy import SQLAlchemy
from flask import g
import urllib2
from lxml import etree

db = SQLAlchemy()


class Deputado(db.Model):
    ideCadastro = db.Column(db.Integer, primary_key=True)
    nomeParlamentar = db.Column(db.String(200))
    nome = db.Column(db.String(200))
    condicao = db.Column(db.String(60))
    uf = db.Column(db.String(3))
    partido = db.Column(db.String(10))
    gabinete = db.Column(db.String(5))
    anexo = db.Column(db.String(5))
    fone = db.Column(db.String(15))
    email = db.Column(db.String(200))
    url_foto = db.Column(db.String(300))
    despesas = db.relationship('Despesa', backref='deputado', lazy='dynamic')

    def __repr__(self):
        return '<Deputado %r>' % (self.nomeParlamentar)

    @classmethod
    def atualiza_database(self):
        data = urllib2.urlopen("http://www.camara.gov.br/SitCamaraWS/Deputados.asmx/ObterDeputados").read()
        deputados = etree.XML(data)

        for deputado in deputados:
            if not Deputado.query.filter_by(ideCadastro=int(deputado.find('ideCadastro').text)).first():
                ideCadastro = int(deputado.find('ideCadastro').text)
                nome = deputado.find('nome').text
                nomeParlamentar = deputado.find('nomeParlamentar').text
                condicao = deputado.find('condicao').text
                uf = deputado.find('uf').text
                partido = deputado.find('partido').text
                gabinete = deputado.find('gabinete').text
                anexo = deputado.find('anexo').text
                fone = deputado.find('fone').text
                email = deputado.find('email').text
                url_foto = deputado.find('urlFoto').text
                dep = Deputado(ideCadastro=ideCadastro, nomeParlamentar=nomeParlamentar, nome=nome, condicao=condicao,
                               uf=uf, partido=partido, gabinete=gabinete, anexo=anexo, fone=fone, email=email,
                               url_foto=url_foto)
                db.session.add(dep)

        db.session.commit()


class Despesa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numRessarcimento = db.Column(db.Integer)
    sgUF = db.Column(db.String(2))
    sgPartido = db.Column(db.String(10))
    txtDescricao = db.Column(db.String(200))
    txtFornecedor = db.Column(db.String(200))
    vlrLiquido = db.Column(db.Float)
    numMes = db.Column(db.Integer)
    numAno = db.Column(db.Integer)
    deputado_id = db.Column(db.Integer, db.ForeignKey('deputado.ideCadastro'))

    @classmethod
    def atualiza_database(self):

        tree = etree.parse("D:\eParlamentar\AnoAtual.xml")
        despesas = tree.getroot()[0]

        for despesa in despesas:

            try:
                numRessarcimento = int(despesa.find('numRessarcimento').text)
            except:
                numRessarcimento = 0
            try:
                sgUF = despesa.find('sgUF').text
            except:
                sgUF = ''
            try:
                sgPartido = despesa.find('sgPartido').text
            except:
                sgPartido = ''
            try:
                txtDescricao = despesa.find('txtDescricao').text
            except:
                txtDescricao = ''
            try:
                vlrLiquido = float(despesa.find('vlrLiquido').text)
            except:
                vlrLiquido = ''
            try:
                numMes = despesa.find('numMes').text
            except:
                numMes = ''
            try:
                numAno = despesa.find('numAno').text
            except:
                numAno = ''
            try:
                txtFornecedor = despesa.find('txtFornecedor').text
            except:
                txtFornecedor = ''
            try:
                deputado_id = int(despesa.find('ideCadastro').text)
            except:
                deputado_id = 0

            deputado = Deputado.query.get(deputado_id)
            d = Despesa(numRessarcimento=numRessarcimento, deputado_id=deputado_id, sgUF=sgUF, sgPartido=sgPartido,
                        txtDescricao=txtDescricao, txtFornecedor=txtFornecedor, vlrLiquido=vlrLiquido, numMes=numMes,
                        numAno=numAno, deputado=deputado)
            db.session.add(d)
        db.session.commit()

    def __repr__(self):
        return '<Despesa %r>' % self.numRessarcimento
