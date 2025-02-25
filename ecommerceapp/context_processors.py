from .models import Cart
from .models import Category

def cart_count(request):
    if request.user.is_authenticated:
        count = Cart.objects.filter(user=request.user).count()
    else:
        count = 0
    return {'cart_count': count}



def categories_context(request):
    categories = Category.objects.all()
    return {'categories': categories}
