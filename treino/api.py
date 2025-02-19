from ninja import Router #importo router
from .schemas import AlunosSchema, AlunoProgessoSchema, AulaRealizadaSchema, AlunosSchema2
from .models import Alunos, AulasConcluidas
from ninja.errors import HttpError
from typing import List
from .graduacao import calculate_lesson_to_upgrade, order_belt
from datetime import date

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
    
    return {
        "email": aluno.email,
        "nome": aluno.nome,
        "faixa": faixa_atual,
        "total_aulas": total_aulas_concluidas_faixa,
        "aulas_necessarios_para_proxima_faixa": aulas_faltantes,
        }

@treino_router.post('/aula_realizada/', response={200: str})
def aula_realizada(request, aula_realizada: AulaRealizadaSchema):
    qtd = aula_realizada.dict()['qtd']
    email_aluno = aula_realizada.dict()['email_aluno']

    if qtd <= 0:
        raise HttpError(400, "Error na quantidade de aulas")
    
    aluno = Alunos.objects.get(email=email_aluno)

    for _ in range(0, qtd):
        ac = AulasConcluidas(
            aluno=aluno,
            faixa_atual=aluno.faixa
        )

    ac.save()
    return 200, f"aula marcada como realizada{aluno.nome}"

@treino_router.put("/alunos/{aluno_id}", response=AlunosSchema2)
def update_aluno(request, aluno_id: int, aluno_data: AlunosSchema2):
    aluno = Alunos.objects.get(id=aluno_id)
    
    idade = date.today() - aluno.data_nascimento

    if int(idade.days/365) < 18 and aluno_data.dict()['faixa'] in ('A', 'R', 'M', 'P'):
        raise HttpError(400, "O aluno é menor de idade e não pode ser graduado para essa faixa.")

    #exclude_unset=True
    for attr, value in aluno_data.dict().items():
        if value:
            setattr(aluno, attr, value)
    
    aluno.save()
    return aluno

@treino_router.delete("/delete/{aluno_id}", response={200: str, 500: str})
def delet_aluno(request, aluno_id: int, email_aluno: str):
    
    try:
        aluno = Alunos.objects.get(id=aluno_id, email=email_aluno)
        aluno.delete()
        return 200, "Usuario excluido com sucesso"
    except Alunos.DoesNotExist:
        raise HttpError("Usuario não encontrado")
