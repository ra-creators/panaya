from django.db import models


class LandingCarousel:
    image = models.ImageField(upload_to='landging/carousel/')

    def __str__(self) -> str:
        return self.image


class ShopCarousel:
    image = models.ImageField(upload_to='shop/carousel/')

    def __str__(self) -> str:
        return self.image

class IndexSlider(models.Model):
    image = models.ImageField(upload_to='index/sliders/')

class ShopSlider(models.Model):
    image = models.ImageField(upload_to='shop/sliders/')
