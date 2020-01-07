from .models import CartItem


def cart_item_middleware(get_response):
    def middleware(request):
        session_key = request.session.session_key
        response = get_response(request)
        if session_key != request.session.session_key:
            CartItem.objects.filter(cart_id=session_key).update(cart_id=request.session.session_key)
        return response
    return middleware
