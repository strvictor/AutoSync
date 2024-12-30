from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def login_usuario(request):
    if request.method == "GET":
        return render(request, 'pagina_login.html')
    
    elif request.method == "POST":
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        # Autenticar usando o email
        usuario = authenticate(request, username=email, password=senha)
        
        if usuario is not None:
            login(request, usuario)
            return redirect('home')
        else:
            # Autenticação falhou
            return render(request, 'pagina_login.html', {'login_errado': 'E-mail ou Senha incorretos!'})