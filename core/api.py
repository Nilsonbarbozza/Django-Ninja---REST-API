from ninja import NinjaAPI #Importar NinjaAPI - para entender que é uma api
from treino.api import treino_router #rota para o app


api = NinjaAPI() #crio uma variavel para encurtar NinjaAPI()
api.add_router('', treino_router) #crio uma nova rota para pg api.py do app + o nome da rota que vou chamar