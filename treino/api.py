from ninja import Router #importo router
from .schemas import AlunosSchema, AlunoProgessoSchema
from .models import Alunos, AulasConcluidas
from ninja.errors import HttpError
from typing import List
from .graduacao import calculate_lesson_to_upgrade, order_belt

treino_router = Router() #Crio uma variavel para encurtar

@treino_router.post('', response={200: AlunosSchema}) #Crio a rota + o methodo ('url')
def criar_aluno(request, aluno_schema: AlunosSchema): #A router acima vai chamar a função que vai realizar a tarefa
    nome = aluno_schema.dict()['nome']
    email = aluno_schema.dict()['email']
    faixa = aluno_schema.dict()['faixa']
    data_nascimento = aluno_schema.dict()['data_nascimento']

    if Alunos.objects.filter(email=email).exists():
        raise HttpError(400, 'Email já cadastrado')
    
    aluno = Alunos(nome=nome,
                    email=email,
                    faixa=faixa,
                    data_nascimento=data_nascimento)
    aluno.save()
    return aluno
@treino_router.get('alunos/', response=List[AlunosSchema])
def listar_alunos(request):
    alunos = Alunos.objects.all()

    return alunos 

@treino_router.get('progresso_aluno/', response={200: AlunoProgessoSchema})
def progresso_aluno(request, email_aluno: str):
    aluno = Alunos.objects.get(email=email_aluno)
    faixa_atual = aluno.get_faixa_display()
    n = order_belt.get(faixa_atual, 0)
    total_aulas_proxima_faixa = calculate_lesson_to_upgrade(n)
    total_aulas_concluidas_faixa = AulasConcluidas.objects.filter(aluno=aluno, faixa_atual=aluno.faixa).count()
    aulas_faltantes = total_aulas_proxima_faixa - total_aulas_concluidas_faixa

    print(aulas_faltantes)
    return {
        "email": aluno.email,
        "nome": aluno.nome,
        "faixa": faixa_atual,
        "total_aulas": total_aulas_concluidas_faixa,
        "aulas_necessarios_para_proxima_faixa": aulas_faltantes,
        }

