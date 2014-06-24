# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from decimal import Decimal
import datetime
from google.appengine.ext import ndb
from gaeforms.ndb.form import ModelForm
from gaeforms.ndb.property import SimpleDecimal, IntegerBounded, SimpleCurrency,FloatBounded


class Participante(ndb.Model):
    nome = ndb.StringProperty(required=True)
    idade = ndb.IntegerProperty(required=True)
    i=IntegerBounded(lower=1,upper=2222222,default=222222)
    ip=ndb.IntegerProperty(default=1)
    fp=ndb.FloatProperty(default=8.3)
    f=FloatBounded(lower=0,upper=100)
    taxa=SimpleDecimal(default=Decimal('1222222.22'))
    salario=SimpleCurrency(default=Decimal('3222222.33'))
    date=ndb.DateProperty(default=datetime.date.today())
    dtime=ndb.DateTimeProperty(default=datetime.datetime.now())


    def to_dict(self,include=None):
        dct = super(Participante, self).to_dict(include=include)
        dct['id'] = self.key.id()
        return dct


class ParticipanteForm(ModelForm):
    _model_class = Participante


def salvar(_json, **ppts):
    participante_form = ParticipanteForm(**ppts)
    errors = participante_form.validate()
    if errors:
        _json(errors,'')
    else:
        participante=participante_form.populate_model()
        participante.put()


def listar(_json):
    query = Participante.query().order(Participante.nome)
    participantes = query.fetch()
    participante_form = ParticipanteForm()
    participantes_dcts = [participante_form.populate_form(p) for p in participantes]
    _json(participantes_dcts, '')


def apagar(id):
    chave = ndb.Key(Participante, int(id))
    chave.delete()