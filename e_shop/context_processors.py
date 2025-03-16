from .models import ServiceCategory

def categories_processor(request):
    """
    Context processor that makes all service categories 
    available to the templates
    """
    return {
        'navbar_categories': ServiceCategory.objects.all()
    }