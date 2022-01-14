from django.contrib import admin
from .models import IndexSlider, ShopSlider

admin.site.register(IndexSlider)
admin.site.register(ShopSlider)

# from .models import LandingCarousel, ShopCarousel


# @admin.register(LandingCarousel)
# class LandingCarouselAdmin(admin.ModelAdmin):
#     pass


# @admin.register(ShopCarousel)
# class ShopCarouselAdmin(admin.ModelAdmin):
#     pass


