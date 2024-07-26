# context_processors.py

from .models import category

def categories_processor(request):
    context={'categories': category.objects.all()}
    return context
