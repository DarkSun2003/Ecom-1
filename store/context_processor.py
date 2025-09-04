from .models import Category

def categories_processor(request):
    """
    A context processor to make categories available globally.
    """
    return {'categories': Category.objects.all()}