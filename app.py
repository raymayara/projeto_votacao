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

class Cadastro(FlaskForm):
    serie = StringField('Série', validators=[DataRequired()])
    turma = StringField('Participantes', validators=[DataRequired()])
    submit = SubmitField('Cadastro')
    
class Criar_votacao(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired()])
    opcoes = StringField('Opção 1')
    opcoes1 = StringField('Opção 2')
    opcoes2 = StringField('Opção 3')
    opcoes3 = StringField('Opção 4')
    opcoes4 = StringField('Opção 5')
    
    submit5 = SubmitField('Criar')
    
class Votacao(db.Model):
    __tablename__="Votacao"
    id = db.Column(db.String(5), primary_key=True, index=True)
    
    titulo= db.Column(db.String (30))
    opcao1= db.Column(db.String (20))
    opcao2= db.Column(db.String (20))
    opcao3= db.Column(db.String (20))
    opcao4= db.Column(db.String (20))
    opcao5= db.Column(db.String (20))
    
    sala = db.relationship('Sala', backref='role')
    
    def __repr__ (self):
        return '<id: %s>' % self.id

class Sala(db.Model):
    __tablename__="Sala"
    id = db.Column(db.String(5), primary_key=True, index=True)
    serie= db.Column(db.String (30))
    turma= db.Column(db.Text (200))
    
    vot_id = db.Column(db.String(5), db.ForeignKey('Votacao.id'))
    
    def __repr__ (self):
        return '<id: %s>' % self.id

@app.route('/', methods=['GET', 'POST'])
def index():
    form = Cadastro()
    
    if form.validate_on_submit():
        db.session.add(Sala(id=str(len(Sala.query.all())+1), serie=form.serie.data, turma=form.turma.data))
        return redirect(url_for('index'))
    
    return render_template('index.html', form=form)
    
@app.route('/criar-votacao', methods=['GET', 'POST'])
def criarVotacao():
    form = Criar_votacao()
    
    return render_template('criarVotacao.html', form=form)
    
@app.route('/votacao-criadas')
def votacaoCriadas():
    return render_template('votacaoCriadas.html')