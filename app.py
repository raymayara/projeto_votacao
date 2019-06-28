import os
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, HiddenField, StringField
from wtforms.validators import DataRequired, NumberRange
#from wtforms.fields.html5 import IntegerField
from wtforms.widgets.html5 import NumberInput
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
#from enum import Enum
# https://devcenter.heroku.com/articles/heroku-postgresql
# https://devcenter.heroku.com/articles/heroku-cli

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'hard to guess string'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
migrate = Migrate(app, db)

def cadastraAlunos(listaDeNomes, serie):
    for nomes in listaDeNomes.split():
        db.session.add(Alunos(aluno=nomes, serie=serie))
        #db.session.commit()

class Cadastro(FlaskForm):
    serie = StringField('Série', validators=[DataRequired()])
    turma = StringField('Participantes', validators=[DataRequired()])
    submit = SubmitField('Cadastro')
    
class Criar_votacao(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired()])
    opcoes = StringField('Opção 1', validators=[DataRequired()])
    opcoes1 = StringField('Opção 2', validators=[DataRequired()])
    opcoes2 = StringField('Opção 3')
    opcoes3 = StringField('Opção 4')
    opcoes4 = StringField('Opção 5')
    
    submit5 = SubmitField('Criar')

class Alunos(db.Model):
    __tablename__="Alunos"
    aluno = db.Column(db.String(64), primary_key=True)
    serie = db.Column(db.String(30), db.ForeignKey('Sala.serie'))

class Votacao(db.Model):
    __tablename__="Votacao"

    titulo= db.Column(db.String (30), primary_key=True)
    opcao1= db.Column(db.String (20))
    opcao2= db.Column(db.String (20))
    opcao3= db.Column(db.String (20))
    opcao4= db.Column(db.String (20))
    opcao5= db.Column(db.String (20))
    
    serie = db.Column(db.String(30), db.ForeignKey('Sala.serie'))
    
    def __repr__ (self):
        return '<titulo: %r>' % self.titulo

class Sala(db.Model):
    __tablename__="Sala"
    serie= db.Column(db.String (30), primary_key=True, index=True)
    
    votacoes = db.relationship('Votacao', backref='Sala')
    alunos = db.relationship('Alunos', backref='Sala')
    
    def __repr__ (self):
        return '<serie: %r;'

@app.route('/', methods=['GET', 'POST'])
def index():
    form = Cadastro()
    votacao = criarVotacao()
    if form.validate_on_submit():
        db.session.add(Sala(serie=form.serie.data)) #cadastra sala
        cadastraAlunos(form.turma.data, serie=form.serie.data) # cadastra alunos
        db.session.commit()# slava aletrações
        return redirect(url_for('criarVotacao', form=votacao))
    
    return render_template('index.html', form=form)
    
@app.route('/criar-votacao', methods=['GET', 'POST'])
def criarVotacao():
    form = Criar_votacao()
    
    if form.validate_on_submit():
        if form.titulo.data != None or form.opcoes.data != None or form.opcoes1.data != None or form.opcoes2.data != None or form.opcoes3.data != None or form.opcoes4.data != None:
            db.session.add(Votacao(titulo=form.titulo.data, opcao1=form.opcoes.data, opcao2=form.opcoes1.data , opcao3=form.opcoes2, opcao4=form.opcoes3.data, opcao5=form.opcoes4.data))
            db.session.commit
    return render_template('criarVotacao.html', form=form)
    
@app.route('/votacao-criadas')
def votacaoCriadas():
    return render_template('votacaoCriadas.html')