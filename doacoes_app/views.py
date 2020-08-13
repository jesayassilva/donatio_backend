from django.contrib.auth.forms import  UserCreationForm,UserChangeForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from .models import *
from .forms import *
from .serializers import *
import json
import jwt
import datetime
from django.views.generic.edit import CreateView

@csrf_exempt
def check_token(token):
    try:
        payload = jwt.decode(token, 'wtcs',algorithm='HS256')
        user = authenticate(request=None,username=payload["username"],password=payload["password"])
    except Exception as e:
        return False

    if user is not None:
        return user
    else:
        return False

@csrf_exempt
def novo_token(username,password):
    user = authenticate(request=None,username=username, password=password)
    if user is not None:
        payload = {
        'username': username,
        'password': password,
        #'exp': datetime.datetime.now() + datetime.timedelta(minutes=60),
        }
        token = jwt.encode(payload, 'wtcs',algorithm='HS256')
        token = str(token)[2:]
        token = token[:-1]
        return token
    else:
        return False

@csrf_exempt #Desabilitar o teste de csrf
def login(request):
    if request.method == "POST":
        try:
            dados = json.loads(request.body.decode("utf-8"))
            token = novo_token(dados["username"],dados["password"])
            usuario = check_token(token)
            #return JsonResponse(usuario.data,safe=False,status=200)
            if token:
                data={
                "token":token,
                "usuario_id":usuario.id
                }
                return JsonResponse(data,safe=False,status=200)
            else:
                return JsonResponse({"Erro":"Credenciais invalidas!"},status=400)
        except Exception as e:
            return JsonResponse({"Erro":"Necessarios username e password"},status=400)
    else:
        return JsonResponse({"Erro":"Apenas o metodo POST"},status=400,safe=False)


@csrf_exempt #Desabilitar o teste de csrf
def todos_produtos(request,tabela):
#---------------------- Checar credenciais

    '''------------REORGANIZAR PQ SE NAO NAO VAI CRIAR USER SEM ESTAR LOGADO
    try:
        token = request.META["HTTP_TOKEN"]
        user = check_token(token)
        if not user:
            return JsonResponse({"Erro":"Credenciais invalidas, Necessario token de authenticacao"},status=400)
    except Exception as e:
        return JsonResponse({"Erro":"Necessario token de authenticacao"},status=400)

    #----------------------Colocando em Maiusculo e Virando codigo python
    '''
    try:
        tabela = str(tabela).capitalize()
        todos_dados = eval(tabela).objects.all()
    except Exception as e:
        return JsonResponse({"Erro":"Url invalida!"},status=400)

    if request.method == 'GET':#Mostra todos os objetos
    #------------------
        try:
            token = request.META["HTTP_TOKEN"]
            user = check_token(token)
            if not user:
                return JsonResponse({"Erro":"Credenciais invalidas, Necessario token de authenticacao"},status=400)
        except Exception as e:
            return JsonResponse({"Erro":"Necessario token de authenticacao"},status=400)
        #----------
        serializer = eval(tabela+"Serializer")(todos_dados,many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":# Cadastra o objeto
        dados = json.loads(request.body.decode("utf-8"))
        if tabela == "User":
            try:
                User.objects.get(username=dados["username"])
                return JsonResponse({'Erro':'username indisponivel'}, status=400)
            except:
                try:
                    if dados["password"] and dados["username"]:
                        user = User.objects.create_user(dados["username"])
                        user.set_password(dados["password"])
                        user.first_name=dados["first_name"]
                        user.last_name=dados["last_name"]
                        user.username=dados["username"]
                        user.email=dados["email"]
                        try:
                            user.save()
                            #return JsonResponse({"Erro":"chegou aki0"},status=400)
                            #perfil = Perfil()
                            #return JsonResponse({"Erro":"chegou aki1"},status=400)
                            perfil = Perfil.objects.get(user=user)

                            perfil.telefone1=dados["telefone1"]
                            perfil.telefone2=dados["telefone2"]
                            perfil.uf=dados["uf"]
                            #return JsonResponse({"Erro":"Aki 3"},status=400)

                            perfil.cidade=dados["cidade"]
                            perfil.endereco=dados["endereco"]
                            perfil.tipo_usuario=dados["tipo_usuario"]
                            perfil.idade=dados["idade"]
                            perfil.save()

                            #criar perfil
                        except Exception as e:
                            return JsonResponse({"Erro":"Dados invalidos"},status=400)
                        serializer =  UserSerializer(User.objects.last())
                        return JsonResponse(serializer.data,status=200)
                except Exception as e:
                    return JsonResponse({"Erro":"Necessario username e password"},status=400)
        else:
        #-----------------
            try:
                token = request.META["HTTP_TOKEN"]
                user = check_token(token)
                if not user:
                    return JsonResponse({"Erro":"Credenciais invalidas, Necessario token de authenticacao"},status=400)
            except Exception as e:
                return JsonResponse({"Erro":"Necessario token de authenticacao"},status=400)
            #-------------------
            form = eval(tabela+"Form")(dados)
        if form.is_valid():
            nova = form.save(commit=False)
            nova.save()
            serializer = eval(tabela+"Serializer")(nova)
            return JsonResponse(serializer.data,safe=False)
        else:
            return JsonResponse({"Erro":"Formulario invalido!"}, status = 400)
    else:
        return JsonResponse({"Erro":"Ultilize somente o metodo GET"},status=400)



@csrf_exempt #Desabilitar o teste de csrf
def cadastro_doacao(request):
    try:
        token = request.POST.get("token")#mandando pelo Formulario
        user = check_token(token)
        usuario = user
        if not user:
            return JsonResponse({"Erro":"Credenciais invalidas, Necessario token de authenticacao"}, status = 400)
    except Exception as e:
        return JsonResponse({"Erro":"Necessario token de authenticacao"}, status = 400)

    doacao = Doacao()
    try:
        produto = Produto.objects.get(pk=request.POST.get("produto"))
    except Exception as e:
        return JsonResponse({"Erro":"codigo do produto invalido"},safe=True,status=400)
    try:
        doacao.doador = usuario
        doacao.produto = produto
        doacao.descricao = request.POST.get("descricao")
        doacao.foto = request.FILES.get("foto")
        serializer = DoacaoSerializer(doacao)
        doacao.save()
        return HttpResponse("<script>location.href='http://localhost/rede/DoacoesOnline/minhas_doacoes2.html'; </script>")
        #return HttpResponse("<script>window.location.assign('file:///home/jesaias/doacoesonlinewebsite/DoacoesOnline/minhas_doacoes2.html')</script>")
        #return HttpResponse("<script>window.location.assign('file:///home/naylson/Documentos/jesaias/DoacoesOnline/nova_doacao.html')</script>")
    except Exception as e:
        return JsonResponse({"Erro":"Formulario invalido"},safe=True,status=400)


def minhas_doacoes(request):
    #---------------------- Checar credenciais
    try:
        token = request.META["HTTP_TOKEN"]
        user = check_token(token)
        usuario = user
        if not user:
            return JsonResponse({"Erro":"Credenciais invalidas, Necessario token de authenticacao"}, status = 400)
    except Exception as e:
        return JsonResponse({"Erro":"Necessario token de authenticacao"}, status = 400)

    try:

        doacoes = Doacao.objects.filter(doador = usuario ).filter(receptor__isnull = True ).order_by('data_criacao')
        i = 0
        lista = []
        for item in doacoes:
            lista.append({
            "id_doacao":item.pk,
            "nome_produto":item.produto.nome,
            "descricao_produto": item.descricao,
            "doador":{"id":item.doador.id,"nome":item.doador.first_name,"sobrenome":item.doador.last_name},
            #"receptor":{"nome":"item.receptor.first_name,"sobrenome":item.receptor.last_name,"email":item.receptor.email},
            #,"uf":item.receptor.uf,"cidade":item.receptor.cidade,"telefone1":item.receptor.telefone1,"telefone2":item.receptor.telefone2
            "data_criacao":str(item.data_criacao)[0:10],
            #"cidade":Perfil.objects.get(user=item.doador.pk).cidade,
            #"uf":Perfil.objects.get(user=item.doador.pk).uf,
            "url_img":item.foto.url,
            "conclusao": "Não"
            })
        return JsonResponse(lista,safe=False)

    except Exception as e:
         return JsonResponse({"Erro":str(e)}, status = 400)
    serializer = DoacaoSerializer(doacoes,many=True)
    return JsonResponse(serializer.data,safe=False)

def minhas_doacoes_solicitadas(request):
    #---------------------- Checar credenciais
    try:
        token = request.META["HTTP_TOKEN"]
        user = check_token(token)
        usuario = user
    except Exception as e:
        return JsonResponse({"Erro":"Necessario token de authenticacao"}, status = 400)

    try:
        #doacoes = Doacao.objects.filter(doador = usuario, conclusao = False ).filter(receptor  ).order_by('data_criacao')
        doacoes = Doacao.objects.filter(doador = usuario, conclusao = False ).filter(receptor__isnull = False ).order_by('data_criacao')
        #doacoes = Doacao.objects.filter(receptor_id =  )#.filter(conclusao = False)#.all()##(doador = usuario).order_by('data_criacao')
        lista = []
        for item in doacoes:
            lista.append({
            "id_doacao":item.pk,
            "nome_produto":item.produto.nome,
            "descricao_produto": item.descricao,
            "doador":{"id":item.doador.id,"nome":item.doador.first_name,"sobrenome":item.doador.last_name},
            "receptor":{"nome":item.receptor.first_name,"sobrenome":item.receptor.last_name,"email":item.receptor.email},
            #,"uf":item.receptor.uf,"cidade":item.receptor.cidade,"telefone1":item.receptor.telefone1,"telefone2":item.receptor.telefone2
            "data_criacao":str(item.data_criacao)[0:10],
            "cidade":Perfil.objects.get(user=item.receptor.pk).cidade,
            "uf":Perfil.objects.get(user=item.receptor.pk).uf,
            "url_img":item.foto.url,
            "telefone1":Perfil.objects.get(user=item.receptor.pk).telefone1,
            "tipo_usuario":Perfil.objects.get(user=item.receptor.pk).tipo_usuario,
            "conclusao": item.conclusao
            })
        return JsonResponse(lista,safe=False)

    except Exception as e:
         return JsonResponse({"Erro":str(e)}, status = 400)
    serializer = DoacaoSerializer(doacoes,many=True)
    return JsonResponse(serializer.data,safe=False)

def minhas_doacoes_finalizadas(request):
    #---------------------- Checar credenciais
    try:
        token = request.META["HTTP_TOKEN"]
        user = check_token(token)
        usuario = user
        if not user:
            return JsonResponse({"Erro":"Credenciais invalidas, Necessario token de authenticacao"}, status = 400)
    except Exception as e:
        return JsonResponse({"Erro":"Necessario token de authenticacao"}, status = 400)

    try:

        doacoes = Doacao.objects.filter(doador = usuario, conclusao = True ).filter(receptor__isnull = False ).order_by('data_criacao')
        i = 0
        lista = []
        for item in doacoes:
            lista.append({
            "id_doacao":item.pk,
            "nome_produto":item.produto.nome,
            "descricao_produto": item.descricao,
            "doador":{"id":item.doador.id,"nome":item.doador.first_name,"sobrenome":item.doador.last_name},
            "receptor":{"nome":item.receptor.first_name,"sobrenome":item.receptor.last_name,"email":item.receptor.email},
            #,"uf":item.receptor.uf,"cidade":item.receptor.cidade,"telefone1":item.receptor.telefone1,"telefone2":item.receptor.telefone2
            "data_criacao":str(item.data_criacao)[0:10],
            "cidade":Perfil.objects.get(user=item.receptor.pk).cidade,
            "uf":Perfil.objects.get(user=item.receptor.pk).uf,
            "url_img":item.foto.url,
            "telefone1":Perfil.objects.get(user=item.receptor.pk).telefone1,
            "tipo_usuario":Perfil.objects.get(user=item.receptor.pk).tipo_usuario,
            "conclusao": item.conclusao
            })
        return JsonResponse(lista,safe=False)

    except Exception as e:
         return JsonResponse({"Erro":str(e)}, status = 400)
    serializer = DoacaoSerializer(doacoes,many=True)
    return JsonResponse(serializer.data,safe=False)

def doacoes_pedidas(request):
    #---------------------- Checar credenciais
    try:
        token = request.META["HTTP_TOKEN"]
        user = check_token(token)
        usuario = user
    except Exception as e:
        return JsonResponse({"Erro":"Necessario token de authenticacao"}, status = 400)

    try:
        #doacoes = Doacao.objects.filter(doador = usuario, conclusao = False ).filter(receptor  ).order_by('data_criacao')
        doacoes = Doacao.objects.filter(receptor = usuario, conclusao = False ).order_by('data_criacao')
        #doacoes = Doacao.objects.filter(receptor_id =  )#.filter(conclusao = False)#.all()##(doador = usuario).order_by('data_criacao')
        lista = []
        for item in doacoes:
            lista.append({
            "id_doacao":item.pk,
            "nome_produto":item.produto.nome,
            "descricao_produto": item.descricao,
            "doador":{"id":item.doador.id,"nome":item.doador.first_name,"sobrenome":item.doador.last_name,"email":item.doador.email},
            "receptor":{"nome":item.receptor.first_name,"sobrenome":item.receptor.last_name,"email":item.receptor.email},
            #,"uf":item.receptor.uf,"cidade":item.receptor.cidade,"telefone1":item.receptor.telefone1,"telefone2":item.receptor.telefone2
            "data_criacao":str(item.data_criacao)[0:10],
            "cidade":Perfil.objects.get(user=item.doador.pk).cidade,
            "uf":Perfil.objects.get(user=item.doador.pk).uf,
            "url_img":item.foto.url,
            "telefone1":Perfil.objects.get(user=item.doador.pk).telefone1,
            "tipo_usuario":Perfil.objects.get(user=item.doador.pk).tipo_usuario,
            "conclusao": item.conclusao
            })
        return JsonResponse(lista,safe=False)

    except Exception as e:
         return JsonResponse({"Erro":str(e)}, status = 400)
    serializer = DoacaoSerializer(doacoes,many=True)
    return JsonResponse(serializer.data,safe=False)

def doacoes_concluidas(request):
    #---------------------- Checar credenciais
    try:
        token = request.META["HTTP_TOKEN"]
        user = check_token(token)
        usuario = user
        if not user:
            return JsonResponse({"Erro":"Credenciais invalidas, Necessario token de authenticacao"}, status = 400)
    except Exception as e:
        return JsonResponse({"Erro":"Necessario token de authenticacao"}, status = 400)

    try:

        doacoes = Doacao.objects.filter(receptor = usuario, conclusao = True ).order_by('data_criacao')
        i = 0
        lista = []
        for item in doacoes:
            lista.append({
            "id_doacao":item.pk,
            "nome_produto":item.produto.nome,
            "descricao_produto": item.descricao,
            "doador":{"id":item.doador.id,"nome":item.doador.first_name,"sobrenome":item.doador.last_name,"email":item.doador.email},
            "receptor":{"nome":item.receptor.first_name,"sobrenome":item.receptor.last_name,"email":item.receptor.email},
            #,"uf":item.receptor.uf,"cidade":item.receptor.cidade,"telefone1":item.receptor.telefone1,"telefone2":item.receptor.telefone2
            "data_criacao":str(item.data_criacao)[0:10],
            "cidade":Perfil.objects.get(user=item.doador.pk).cidade,
            "uf":Perfil.objects.get(user=item.doador.pk).uf,
            "url_img":item.foto.url,
            "telefone1":Perfil.objects.get(user=item.doador.pk).telefone1,
            "tipo_usuario":Perfil.objects.get(user=item.doador.pk).tipo_usuario,
            "conclusao": item.conclusao
            })
        return JsonResponse(lista,safe=False)

    except Exception as e:
         return JsonResponse({"Erro":str(e)}, status = 400)
    serializer = DoacaoSerializer(doacoes,many=True)
    return JsonResponse(serializer.data,safe=False)


def doacoes(request):
    #---------------------- Checar credenciais
    try:
        token = request.META["HTTP_TOKEN"]
        user = check_token(token)
        if not user:
            return JsonResponse({"Erro":"Credenciais invalidas, Necessario token de authenticacao"}, status = 400)
    except Exception as e:
        return JsonResponse({"Erro":"Necessario token de authenticacao"}, status = 400)

    try:
        #Entry.objects.order_by(Lower('headline').desc())
        doacoes = Doacao.objects.filter(conclusao = False, receptor = None ).order_by('data_criacao')
        i = 0
        lista = []
        for item in doacoes:
            lista.append({
            "id_doacao":item.pk,
            "nome_produto":item.produto.nome,
            "descricao_produto": item.descricao,
            "doador":{"id":item.doador.id,"nome":item.doador.first_name,"sobrenome":item.doador.last_name, "email":item.doador.email},
            "data_criacao":str(item.data_criacao)[0:10],
            "cidade":Perfil.objects.get(user=item.doador.pk).cidade,
            "uf":Perfil.objects.get(user=item.doador.pk).uf,
            "url_img":item.foto.url,
            "telefone1":Perfil.objects.get(user=item.doador.pk).telefone1,
            "tipo_usuario":Perfil.objects.get(user=item.doador.pk).tipo_usuario
            })
        return JsonResponse(lista,safe=False)

    except Exception as e:
         return JsonResponse({"Erro":"Erro"}, status = 400)
    serializer = DoacaoSerializer(doacoes,many=True)
    return JsonResponse(serializer.data,safe=False)

def doacoes_categoria(request,pk):
    #---------------------- Checar credenciais

    try:
        token = request.META["HTTP_TOKEN"]
        user = check_token(token)
        if not user:
            return JsonResponse({"Erro":"Credenciais invalidas, Necessario token de authenticacao"}, status = 400)
    except Exception as e:
        return JsonResponse({"Erro":"Necessario token de authenticacao"}, status = 400)

    try:
        categoria = Categoria.objects.get(pk=pk)
        doacoes = Doacao.objects.filter(conclusao = False, receptor = None, produto__categoria = categoria ).order_by('data_criacao')
        i = 0
        lista = []
        for item in doacoes:
            lista.append({
            "id_doacao":item.pk,
            "nome_produto":item.produto.nome,
            "descricao_produto": item.descricao,
            "doador":{"nome":item.doador.first_name,"sobrenome":item.doador.last_name},
            "data_criacao":str(item.data_criacao)[0:10],
            "cidade":Perfil.objects.get(user=item.doador.pk).cidade,
            "uf":Perfil.objects.get(user=item.doador.pk).uf,
            "url_img":item.foto.url,
            "telefone1":Perfil.objects.get(user=item.doador.pk).telefone1,
            "tipo_usuario":Perfil.objects.get(user=item.doador.pk).tipo_usuario
            })
        if lista==[]:
             return JsonResponse({"Erro":"Nenhum produto encontrado nessa Categoria"}, status = 400)
        return JsonResponse(lista,safe=False)

    except Exception as e:
         return JsonResponse({"Erro":str(e)}, status = 400)
    serializer = DoacaoSerializer(doacoes,many=True)
    return JsonResponse(serializer.data,safe=False)

@csrf_exempt #Desabilitar o teste de csrf
def pesquisa_doacao(request):
    #---------------------- Checar credenciais
    dados = json.loads(request.body.decode("utf-8"))
    try:
        token = request.META["HTTP_TOKEN"]
        user = check_token(token)
        if not user:
            return JsonResponse({"Erro":"Credenciais invalidas, Necessario token de authenticacao"}, status = 400)
    except Exception as e:
        return JsonResponse({"Erro":"Necessario token de authenticacao"}, status = 400)

    try:

        #Entry.objects.get(headline__contains='Lennon')
        doacoes = Doacao.objects.filter(conclusao = False, receptor = None, produto__nome__contains = dados["nome_produto"] ).order_by('data_criacao')
        i = 0
        lista = []
        for item in doacoes:
            lista.append({
            "id_doacao":item.pk,
            "nome_produto":item.produto.nome,
            "descricao_produto": item.descricao,
            "doador":{"nome":item.doador.first_name,"sobrenome":item.doador.last_name},
            "data_criacao":str(item.data_criacao)[0:10],
            "cidade":Perfil.objects.get(user=item.doador.pk).cidade,
            "uf":Perfil.objects.get(user=item.doador.pk).uf,
            "url_img":item.foto.url,
            "telefone1":Perfil.objects.get(user=item.doador.pk).telefone1,
            "tipo_usuario":Perfil.objects.get(user=item.doador.pk).tipo_usuario
            })
        if lista==[]:
             return JsonResponse({"Erro":"Nenhum produto encontrado para doacao"}, status = 400)
        return JsonResponse(lista,safe=False)

    except Exception as e:
         return JsonResponse({"Erro":str(e)}, status = 400)
    serializer = DoacaoSerializer(doacoes,many=True)
    return JsonResponse(serializer.data,safe=False)


@csrf_exempt #Desabilitar o teste de csrf
def especifico_produto(request,tabela,pk): #Objeto especifico
    #---------------------- Checar credenciais
    try:
        token = request.META["HTTP_TOKEN"]
        user = check_token(token)
        if not user:
            return JsonResponse({"Erro":"Credenciais invalidas, Necessario token de authenticacao"}, status = 400)
    except Exception as e:
        return JsonResponse({"Erro":"Necessario token de authenticacao"}, status=400)

    #---------------------- Procurando
    try:
        tabela = str(tabela).capitalize()
        item = eval(tabela).objects.get(pk=pk)# fazendo pesquisa do objeto
    except Exception as e:
        return JsonResponse({"Erro":"Erro na url ou o ID nao exite"},status=400)

    if request.method =="GET": #Mostra objeto especifico pelo id
        serializer = eval(tabela+"Serializer")(item,many=True)
        return JsonResponse(serializer.data,safe=False)

    elif request.method == "POST":#ALterar objeto especifico
        try:
            dados = json.loads(request.body.decode("utf-8"))

            if tabela =="Produto":
                try:
                    item.nome = dados["nome"]
                    item.categoria = Categoria.objects.get(pk= str(dados["categoria"]))
                except Exception as e:
                    serializer = CategoriaSerializer(Categoria.objects.all(),many=True)
                    data={
                        "Disponiveis":serializer.data,
                        "Erro":"Necessarios os campos nome e categoria,Escolha uma das categoria",
                    }
                    return JsonResponse(data,status=400)

            if tabela=='User':
                try:
                    item.first_name=dados["first_name"]
                    item.last_name=dados["last_name"]
                    item.username=dados["username"]
                    item.email=dados["email"]
                    item.save()
                    return JsonResponse({'Msg':'Atualizado com sucesso!'}, status=200)
                except Exception as e:
                    return JsonResponse({'Erro':'Necessario: username,first_name,last_name,email !'}, status=200)

            if tabela == "Categoria":
                try:
                    item.descricao = dados["descricao"]
                except Exception as e:
                    return JsonResponse({"Erro":"Necessario o campo descricao"})
                item.save()
                serializer = eval(tabela+"Serializer")(item)
                return JsonResponse(serializer.data,safe=False)
            #alterar doacao{
            if tabela == "Doacao":

                try:
                    #item.doador = Doador.objects.get(pk = dados["doador"])
                    item.receptor = User.objects.get(pk = dados["receptor"] )
                    item.produto = Produto.objects.get(pk = dados["produto"])
                    #item.data_criacao = dados["data_criacao"]
                    item.data_conclusao = dados["data_conclusao"]
                    item.conclusao = dados["conclusao"]
                    item.foto = dados["foto"]
                    item.descricao = dados["descricao"]
                    item.save()
                    serializer = eval(tabela+"Serializer")(item)
                except Exception as e:
                    return JsonResponse({"Erro":"Erro ao atualizarr"})
                    #return JsonResponse({"Erro":str(e)})
                return JsonResponse(serializer.data,safe=False)
        #}alterar doacao '''
        except Exception as e:
            #return JsonResponse({"Erro":"Falha ao Atualizar"},status=400)
            return JsonResponse({"Erro":str(e)})

    elif request.method == "DELETE":
        try:
            item.delete()
            return JsonResponse({'Msg':'Deletado com sucesso!'},status=200)
        except:
            return JsonResponse({'Erro':'Nao foi possivel deletar'},status=400)
def euquero(request,id_doacao):
    #---------------------- Checar credenciais
    try:
        token = request.META["HTTP_TOKEN"]
        user = check_token(token)
        if not user:
            return JsonResponse({"Erro":"Credenciais invalidas, Necessario token de authenticacao"}, status = 400)
    except Exception as e:
        return JsonResponse({"Erro":"Necessario token de authenticacao"}, status = 400)
    try:
        doacao = Doacao.objects.get(pk=id_doacao)
        #return HttpResponse(doacao)
        if doacao.doador == user:
            return JsonResponse({"Erro":"Você não pode solicitar sua propria doação"}, status = 400)
        #return JsonResponse({"Erro":"aqui mesmo"}, status = 400)
        doacao.receptor = user
        doacao.save()
        return JsonResponse({"Msg":"Doação Solicitada"}, status = 200)
    except Exception as e:
        return JsonResponse({"Erro":"Erro ao salvar"}, status = 400)


def aceitar_doacao(request,id_doacao):
    #---------------------- Checar credenciais
    try:
        token = request.META["HTTP_TOKEN"]
        user = check_token(token)
        if not user:
            return JsonResponse({"Erro":"Credenciais invalidas, Necessario token de authenticacao"}, status = 400)
    except Exception as e:
        return JsonResponse({"Erro":"Necessario token de authenticacao"}, status = 400)
    try:
        doacao = Doacao.objects.get(pk=id_doacao)
        #return HttpResponse(doacao)
        doacao.conclusao = True
        #doacao.data_conclusao = datetime.now
        doacao.save()
        return JsonResponse({"Msg":"Doado com Sucesso"}, status = 200)
    except Exception as e:
        return JsonResponse({"Erro":"Erro ao doar"}, status = 400)

def recusar_doacao(request,id_doacao):
    #---------------------- Checar credenciais
    try:
        token = request.META["HTTP_TOKEN"]
        user = check_token(token)
        if not user:
            return JsonResponse({"Erro":"Credenciais invalidas, Necessario token de authenticacao"}, status = 400)
    except Exception as e:
        return JsonResponse({"Erro":"Necessario token de authenticacao"}, status = 400)
    try:
        doacao = Doacao.objects.get(pk=id_doacao)
        #return HttpResponse(doacao)
        doacao.receptor = None
        #doacao.data_conclusao = datetime.now
        doacao.save()
        return JsonResponse({"Msg":"Recusado com sucesso"}, status = 200)
    except Exception as e:
        return JsonResponse({"Erro":"Erro ao salvar"}, status = 400)

def estatisticas(request):
    #---------------------- Checar credenciais
    try:
        token = request.META["HTTP_TOKEN"]
        user = check_token(token)
        if not user:
            return JsonResponse({"Erro":"Credenciais invalidas, Necessario token de authenticacao"}, status = 400)
    except Exception as e:
        return JsonResponse({"Erro":"Necessario token de authenticacao"}, status = 400)

    try:
        doacoes = Doacao.objects.filter(conclusao = True, doador = user )
        minhas_doacoes = 0
        for item in doacoes:
            minhas_doacoes = minhas_doacoes+1

        doacoes = Doacao.objects.filter(conclusao = True, receptor = user )
        minhas_solicitacoes = 0
        for item in doacoes:
            minhas_solicitacoes = minhas_solicitacoes+1

        doacoes = Doacao.objects.filter(conclusao = True)
        doacoes_site = 0
        for item in doacoes:
            doacoes_site = doacoes_site+1

        doacoes = Doacao.objects.filter(conclusao = False, receptor = None )
        doacoes_disponiveis = 0
        for item in doacoes:
            doacoes_disponiveis = doacoes_disponiveis+1

        doacoes = Doacao.objects.filter(conclusao = False).filter(receptor__isnull = False )
        doacoes_pendentes = 0
        for item in doacoes:
            doacoes_pendentes = doacoes_pendentes+1


        doacoes = Doacao.objects.filter(conclusao = True)
        doacoes_pessoa_jurudica = 0
        for item in doacoes:
            if Perfil.objects.get(user=item.receptor.pk).tipo_usuario == "Pessoa Jurídica":
                doacoes_pessoa_jurudica = doacoes_pessoa_jurudica+1

        doacoes = Doacao.objects.filter(conclusao = True)
        doacoes_pessoa_fisica = 0
        for item in doacoes:
            if Perfil.objects.get(user=item.receptor.pk).tipo_usuario == "Pessoa Física":
                doacoes_pessoa_fisica = doacoes_pessoa_fisica+1


        dados = {
        "minhas_doacoes": minhas_doacoes,
        "minhas_solicitacoes" : minhas_solicitacoes,
        "doacoes_site" : doacoes_site,
        "doacoes_pessoa_jurudica" : doacoes_pessoa_jurudica,
        "doacoes_pessoa_fisica" : doacoes_pessoa_fisica,
        "doacoes_disponiveis" : doacoes_disponiveis,
        "doacoes_pendentes" : doacoes_pendentes


        #'exp': datetime.datetime.now() + datetime.timedelta(minutes=60),
        }
        return JsonResponse(dados,safe=False)
    except Exception as e:
         return JsonResponse({"Erro":str(e)}, status = 400)
    serializer = DoacaoSerializer(doacoes,many=True)
    return JsonResponse(serializer.data,safe=False)
