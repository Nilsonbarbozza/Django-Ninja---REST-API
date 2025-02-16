from ninja import Router #importo router
from .schemas import AlunosSchema
from .models import Alunos

treino_router = Router() #Crio uma variavel para encurtar

@treino_router.post('', response={200: AlunosSchema}) #Crio a rota + o methodo ('url')
def criar_aluno(request, aluno_schema: AlunosSchema): #A router acima vai chamar a função que vai realizar a tarefa
    nome = aluno_schema.dict()['nome']
    email = aluno_schema.dict()['email']
    faixa = aluno_schema.dict()['faixa']
    data_nascimento = aluno_schema.dict()['data_nascimento']

    aluno = Alunos(nome=nome,
                    email=email,
                    faixa=faixa,
                    data_nascimento=data_nascimento)
    aluno.save()
    return aluno

