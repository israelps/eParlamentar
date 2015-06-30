from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
import urllib2
from urllib import urlretrieve
import zipfile
import os
from lxml import etree

db = SQLAlchemy()


class Deputado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_parlamentar = db.Column(db.String(200))
    nome = db.Column(db.String(200))
    condicao = db.Column(db.String(60))
    uf = db.Column(db.String(3))
    partido = db.Column(db.String(10))
    gabinete = db.Column(db.String(5))
    anexo = db.Column(db.String(5))
    fone = db.Column(db.String(15))
    email = db.Column(db.String(200))
    url_foto = db.Column(db.String(300))
    ultima_atualizacao = db.Column(db.DateTime)
    despesas = db.relationship('Despesa', backref='deputado', lazy='dynamic')

    def __repr__(self):
        return '<Deputado %r>' % (self.nome_parlamentar)

    @classmethod
    def atualiza_database(self):
        db.drop_all()
        db.create_all()
        data = urllib2.urlopen("http://www.camara.gov.br/SitCamaraWS/Deputados.asmx/ObterDeputados").read()
        deputados = etree.XML(data)

        for deputado in deputados:
            if not Deputado.query.get(int(deputado.find('ideCadastro').text)):
                id = int(deputado.find('ideCadastro').text)
                nome = deputado.find('nome').text
                nome_parlamentar = deputado.find('nomeParlamentar').text
                condicao = deputado.find('condicao').text
                uf = deputado.find('uf').text
                partido = deputado.find('partido').text
                gabinete = deputado.find('gabinete').text
                anexo = deputado.find('anexo').text
                fone = deputado.find('fone').text
                email = deputado.find('email').text
                url_foto = deputado.find('urlFoto').text
                dep = Deputado(id=id, nome_parlamentar=nome_parlamentar, nome=nome, condicao=condicao,
                               uf=uf, partido=partido, gabinete=gabinete, anexo=anexo, fone=fone, email=email,
                               url_foto=url_foto, ultima_atualizacao=datetime.today())
                db.session.add(dep)

        db.session.commit()


class Despesa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num_ressarcimento = db.Column(db.Integer)
    uf = db.Column(db.String(2))
    partido = db.Column(db.String(10))
    descricao = db.Column(db.String(200))
    fornecedor = db.Column(db.String(200))
    valor = db.Column(db.Float)
    mes = db.Column(db.Integer)
    ano = db.Column(db.Integer)
    num_subcota = db.Column(db.Integer)
    deputado_id = db.Column(db.Integer, db.ForeignKey('deputado.id'))

    @classmethod
    def atualiza_database(self):

        if os.environ.get('OPENSHIFT_TMP_DIR'):
            url = 'http://www.camara.gov.br/cotas/AnoAtual.zip'
            path = os.environ.get('OPENSHIFT_TMP_DIR')
            urlretrieve(url, path)
            with zipfile(path+'AnoAtual.zip') as zf:
                zf.extractall(path)
        else:
            path = "D:\\eParlamentar\\"

        tree = etree.parse(path + "AnoAtual.xml")
        despesas = tree.getroot()[0]

        for despesa in despesas:

            try:
                num_ressarcimento = int(despesa.find('numRessarcimento').text)
            except:
                num_ressarcimento = 0
            try:
                uf = despesa.find('sgUF').text
            except:
                uf = ''
            try:
                num_subcota = despesa.find('numSubCota').text
            except:
                num_subcota = ''
            try:
                partido = despesa.find('sgPartido').text
            except:
                partido = ''
            try:
                descricao = despesa.find('txtDescricao').text
            except:
                descricao = ''
            try:
                valor = float(despesa.find('vlrLiquido').text)
            except:
                valor = ''
            try:
                mes = despesa.find('numMes').text
            except:
                mes = ''
            try:
                ano = despesa.find('numAno').text
            except:
                ano = ''
            try:
                fornecedor = despesa.find('txtFornecedor').text
            except:
                fornecedor = ''
            try:
                deputado_id = int(despesa.find('ideCadastro').text)
            except:
                deputado_id = 0

            deputado = Deputado.query.get(deputado_id)
            d = Despesa(num_ressarcimento=num_ressarcimento, num_subcota=num_subcota, deputado_id=deputado_id, uf=uf,
                        partido=partido,
                        descricao=descricao, fornecedor=fornecedor, valor=valor, mes=mes,
                        ano=ano, deputado=deputado)
            db.session.add(d)
        db.session.commit()

    def __repr__(self):
        return '<Despesa %r>' % self.num_ressarcimento
