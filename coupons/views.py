import json
from django.http.response import HttpResponse, JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Coupon
from cart.cart import Cart

# Create your views here.

@require_POST
@csrf_exempt
def coupon_apply(request):
    now = timezone.now()
    code = request.POST.get('code')
    # print(code)
    if code:
        try:
            coupon = Coupon.objects.get(code__iexact=code,
                                        valid_from__lte=now,
                                        valid_to__gte=now, 
                                        active=True)
            request.session['coupon_id'] = coupon.id
            cart = Cart(request)
            
            # check if after discount total is above threshold
            check_dis = cart.check_discount(coupon)
            if cart.get_total_price() - check_dis < 1:
                request.session['coupon_id'] = None
                return HttpResponse(404)

            dic = {
                'status': 'success',
                'discount': int(coupon.discount),
                'total': str(cart.get_total_price_after_discount())
            }            
            return JsonResponse(json.dumps(dic), safe=False)
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
            return HttpResponse(404)