from django.shortcuts import render

def index(request):
    texts = ['Lorem ipsum dolor', 'sit amet consectetur']
    context = {
        'title': 'Django E-commerce',
        'texts': texts
    }
    return render(request, 'index.html', context)

def contato(request):
    return render(request, 'contato.html')

def produto(request):
    return render(request, 'produto.html')

def lista_produto(request):
    return render(request, 'lista_produtos.html')