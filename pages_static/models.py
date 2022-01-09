from django.db import models


class LandingCarousel:
    image = models.ImageField(upload_to='landging/carousel/')

    def __str__(self) -> str:
        return self.image


class ShopCarousel:
    image = models.ImageField(upload_to='shop/carousel/')

    def __str__(self) -> str:
        return self.image
