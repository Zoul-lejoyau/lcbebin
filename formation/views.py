from django.shortcuts import render
from django.views.generic import DetailView
from django.db.models import Q
from django.contrib import messages


from .models import Category, Formation


def home(request):
    topFormations = Formation.objects.all()
    return render(request, 'formation/index.html', {
    'topFormations': topFormations,
    'title': 'Home'
    })


def about(request):
    return render(request, 'formation/about.html', {'title': 'About'})


class FormationDetail(DetailView):
    model = Formation
    template_name = 'formation/formationDetail.html'

def search(request):
    query = request.GET.get('query', '')

    if query:
        formations = Formation.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query))

        return render(request, 'formation/search.html', {
            'formations': formations,
            'title': 'Search',
            'query': query
        })
    else:

        return render(request, 'formation/search.html', {
            'formations': [],
            'messages': messages.success(request, f'pas de trouvé')
        })
