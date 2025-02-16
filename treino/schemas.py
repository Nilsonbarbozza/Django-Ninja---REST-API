from ninja import ModelSchema, Schema
from .models import Alunos

class AlunosSchema(ModelSchema):
    class Meta:
        model = Alunos
        fields = ['nome', 'email', 'faixa', 'data_nascimento']

class AlunoProgessoSchema(Schema):
    email: str
    nome: str
    faixa: str 
    total_aulas: str
    aulas_necessarios_para_proxima_faixa: int