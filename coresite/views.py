from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404 
from django.http import HttpResponse 
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.models import User #Trazendo os modelo que ja existem no django (email, username e parssword)
from django.contrib.auth import authenticate #Função que verifica direto no banco se as informções são iguais as digitadas 

#Inportando controle de segurança para acesso as paginas
from django.contrib.auth.decorators import login_required #Ipede que usuarios não autenticado acesse as views
from django.core.exceptions import PermissionDenied

from django.contrib.auth import logout as logout_django
from django.contrib.auth import login as login_django
#Como nossa própria função def () também chama login, precisamos
#renomear a função nativa do
#Django para login_django usando
#a palavra-chave as para evitar
#conflitos no código

#Model inportados.
from .models import Nota




# Create your views here.

#Função para redenrizar uma pagina web
def home(request):
    return render(request, 'login.html')


def erro(request):
    return render(request, 'error.html')


#-----------------Funções com restrição de acesso-----------------------

#Função para renderizar a pagina adminstrativa se não tive autenticado evia para uma pagina de erro
@login_required(login_url='erro')
def admin(request):
    return render(request, 'admin.html')

#Desa forma a função so e acessada se o usuario estiver autenticado 
#def admin(request):
    #if not request.user.is_authenticated:
       #raise PermissionDenied
    #return render(request, 'admin.html')


#----------------fim----------------------------------------------------

#Função para sair do sistema
def logout(request):
    if request.user.is_authenticated:
        logout_django(request)
        return redirect('home')
    else:
        return HttpResponse('Você não acessou sua conta ainda!')


#Função para cadastrar usuarios
def cad_usuario(request):
    if request.method == 'GET':
        return redirect('home')
    else:
        username = request.POST.get('email')
        email = request.POST.get('email')
        password = request.POST.get('senha')
        first_name = request.POST.get('nome')

        user = User.objects.filter(username=username).first()

        if user:
            return HttpResponse('Usuário ja existe')
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name
            )
            user.save()
            messages.success(request, 'Usuário cadastrado com sucesso!')
            return redirect('/')
        

#Função para logar no sistema
def login(request):
    if request.method == 'GET':
        return redirect('home')
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']
        user  = authenticate(request, username=email, password=senha)#Autenticando o usuario    
            
    if user is not None:#Verifica se o usuario foi encontrado
        login_django(request, user)#Inicia a seção do usuario
        #return HttpResponse('Usuário autenticado com sucesso!')       
        return redirect('pag_admin')                 
    else:
        messages.error(request, 'Email e senha inválidos!')
        return redirect('/') 
    

#------Funções para cadastro ---------

#Função para lançar notas no sistema
@login_required(login_url='erro')
def lancarNotas(request):
    if request.method =='GET':
        if request.user.is_authenticated:
            return render(request, 'lancarNotas.html')
        else:
            return HttpResponse('Faça o login para acessar!')
    else:
        nota = Nota()#Cria um objeto da class Nota
        nota.nome_aluno = request.user.first_name #Insere o nome de quem esta autenticado
        nota.disciplina = request.POST.get('disciplina').upper()#Atributos da class rebendo dados do fumulario
        nota.nota_atividade = request.POST.get('nota_atividade')
        nota.nota_trabalho = request.POST.get('nota_trabalho')
        nota.nota_prova = request.POST.get('nota_prova')

        #Calculo da mnédia
        nota.media = (
            int(nota.nota_atividade) + 
            int(nota.nota_trabalho) + 
            int(nota.nota_prova)
            )/3 #Soma as notas 

        nota_verificada = Nota.objects.filter(disciplina=nota.disciplina).first()#Verifica se ja foi cadastrada notas para essa disciplina

        if nota_verificada:
            return HttpResponse('Disciplina já possui notas cadastradas!')
        else:           
            nota.save() #Salva as nota no BD 

            messages.success(request, 'Lançamento feito com sucesso!')           
            return render(request, 'admin.html')#Retorna para pagina administrativa
        

#------Funções para consultar e visualizar dados no Banco de Dados ---------
@login_required(login_url='erro')
def visualizar(request):
    if request.method == 'GET':# Verifica se o método da requisição é GET (quando o usuário acessa a página normalmente)
        if request.user.is_authenticated: # Verifica se o usuário está autenticado (ou seja, se está logado no sistema)
            #ista_notas = Nota.objects.all()
            lista_notas = Nota.objects.filter(nome_aluno=request.user.first_name)#Faz uma consulta na tabela Nota, Retorna todos os registros
            dicionario_nota = {'lista_notas':lista_notas}#Cria um dicionário para enviar dados ao template, lista_notas será usada no HTML
            return render(request, 'visualizarNotas.html', dicionario_nota)#Renderiza a página HTML, Envia os dados para o template
        else:
            return HttpResponse('Faça o login para acessar! ') #Retorna uma mensagem no navegador
        
    else:
        disciplina = request.POST.get('disciplina')# Pega o valor do campo 'disciplina' enviado pelo formulário HTML

        if disciplina == 'Todas as disciplinas':# Verifica se o usuário escolheu ver todas as disciplinas
            lista_notas = Nota.objects.all()# Consulta o banco e retorna todas as notas
        else:
            lista_notas = Nota.objects.filter(disciplina=disciplina)  # Filtra os registros da tabela Nota baseado na disciplina selecionada

        dicionario_nota = {'lista_notas': lista_notas}# Cria o dicionário com os dados filtrados (ou completos)

        return render(request, 'visualizarNotas.html', dicionario_nota)# Renderiza o mesmo template HTML, agora com os dados filtrados


#Funçao para lista dados para ser alterado ou exluidos 
@login_required(login_url='erro')
def alterar(request):
    if request.user.is_authenticated:
        lista_notas = Nota.objects.all()
        dicionario_notas = {'lista_notas': lista_notas}
        return render(request, 'alterarNota.html', dicionario_notas)
    else:
       return HttpResponse('Faça o login para acessar! ')
    

# ------ Função para altera dados no Banco de Dados ---------

#Função que verificar o dado que vai ser alterado e direciona para pagina de edição
@login_required(login_url='erro')
def editar_verificacao(request, pk):
    if request.method == 'GET':
        if request.user.is_authenticated:
            lista_notas = Nota.objects.get(pk=pk)
            dicionario_notas = {'lista_notas': lista_notas}
            return render(request, 'editar.html', dicionario_notas)#Direciona para pagina para confirma a edição dos dados
        else:
            return HttpResponse('Faça o login para acessar! ')


#Função que salva os dados alterados
@login_required(login_url='erro')
def editar(request, pk):
    
    if request.method == "POST":
        
        nome_aluno = request.user.first_name
        disciplina = request.POST.get('disciplina')
        nota_atividade = request.POST.get('nota_atividade')
        nota_trabalho = request.POST.get('nota_trabalho')
        nota_prova = request.POST.get('nota_prova')

        # cálculo da média
        media = (
            int(nota_atividade) +
            int(nota_trabalho) +
            int(nota_prova)
        )/3

        # atualiza no banco
        Nota.objects.filter(pk=pk).update(
            nome_aluno=nome_aluno,
            disciplina=disciplina,
            nota_atividade=nota_atividade,
            nota_trabalho=nota_trabalho,
            nota_prova=nota_prova,
            media=media
        )
        messages.success(request, 'Nota Alterada com sucesso!')
        return HttpResponseRedirect(reverse('alterar'))

    # caso não seja POST
    return HttpResponseRedirect(reverse('pag_admin'))

# ------ Função para deletar dados no Banco de Dados ---------

#Função que verificar o dado a ser delatado na pagina altera nota 
@login_required(login_url='erro')
def excluir_verificacao(request, pk):
    if request.method == 'GET':
        if request.user.is_authenticated:
            lista_notas = Nota.objects.get(pk=pk)
            dicionario_notas = {'lista_notas': lista_notas}
            return render(request, 'excluir.html', dicionario_notas)#Direciona para pagina para confirma a exclusão
        else:
            return HttpResponse('Faça o login para acessar! ')


#Exlui o dado definitivamente vindo da pagina altera nota
@login_required(login_url='erro')
def excluir(request, pk):
    if request.method == 'GET':
        if request.user.is_authenticated:
            disciplina_selencionada = Nota.objects.get(pk=pk)
            disciplina_selencionada.delete()

            messages.error(request, 'Nota excluida com sucesso!')
            return HttpResponseRedirect(reverse('alterar'))
        else:
            return HttpResponse('Faça o login para acessar!')


#Função que deleta direto na pagina Visualizar notas 
@login_required(login_url='erro') # Garante que apenas usuários logados acessem a função
def deletar_nota(request, id_nota):
    # Busca a nota pelo ID (chave primária) ou retorna um erro 404 caso não exista
    nota = get_object_or_404(Nota, pk=id_nota)
    
    if request.method == 'POST':
        nota.delete() # Deleta o registro do banco de dados
        messages.error(request, 'Nota deletada com sucesso!')
        return redirect('pag_admin') # Redireciona de volta para a lista de notas
        
    # Se o usuário tentar acessar via GET (acesso direto pela URL), 
    # enviamos ele para uma página de confirmação antes de apagar
    return render(request, 'pag_admin')




