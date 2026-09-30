from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),

    #Rota da pagina de erro  
    path('erro/', views.erro, name='erro'),

    #Rota pa sair do sistema
    path('logout/', views.logout, name='logout'),

    #rota pagina de login  
    path('login/', views.login, name='login'),#Pagina de login

    #Rota para pagina de cadstro de usuario
    path('usuario/', views.cad_usuario, name='usuario'), #Pagina de cadastro de usuario

    #Rota para sistema de Adminstração (esta protegida so tem acesso quem esta autenticado)
    path('pag_admin/', views.admin, name='pag_admin'),#Pagina painel administrativo

    #Rota para pagina de cadastro de notas (esta protegida so tem acesso quem esta autenticado)
    path('lancar/', views.lancarNotas, name='lancar'),#Pagina lançar nota

    #Rota para visualizar (esta protegida so tem acesso quem esta autenticado)
    path('visualizar/', views.visualizar, name='visualizar'),

    #Rota para alterar
    path('alterar/', views.alterar, name='alterar'),

    #-------- Rotas para alterar--------- 
    #Verificada o dado a ser alterado
    path('editar_verificacao/<int:pk>', views.editar_verificacao, name='editar_verificacao'),

    #Salva o dados que foram alterados 
    path('editar/<int:pk>', views.editar, name='editar'),

    #-------- Rotas para deletar--------- 

    #Deletar direto na pagina visualizar notas
    path('deletar_nota/<int:id_nota>/', views.deletar_nota, name='deletar_nota'),

    #Verificarar ante de excluir
    path('excluir_verificacao/<int:pk>', views.excluir_verificacao, name='excluir_verificacao'),

    #Excluir o dado escolhido
    path('excluir/<int:pk>', views.excluir, name='excluir'),
]
