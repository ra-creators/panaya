from itertools import chain
from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()
# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)

    class Meta:
        ordering = ('name', )
        verbose_name = 'tag'
        verbose_name_plural = 'tags'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    thumbnail = models.ImageField(
        upload_to='products/categories/%Y/%m/%d', blank=True,
        default="/media/defaults/noimg.png")

    class Meta:
        ordering = ('name', )
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    @property
    def get_thumbnail(self):
        if self.thumbnail:
            return ("https://static.panaya.in/media/" + str(self.thumbnail))
        else:
            return "https://static.panaya.in/media/defaults/noimg.png"

    def get_absolute_url(self):
        return reverse('product_list_by_category',
                       args=[self.slug])


class Collection(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    thumbnail = models.ImageField(
        blank=True,
        default="/media/defaults/noimg.png",
        upload_to='products/collections/%Y/%m/%d',
    )

    class Meta:
        ordering = ('name', )
        verbose_name = 'collection'
        verbose_name_plural = 'collections'

    def __str__(self):
        return self.name

    @property
    def get_thumbnail(self):
        if self.thumbnail:
            return ("https://static.panaya.in/media/" + str(self.thumbnail))
        else:
            return "https://static.panaya.in/media/defaults/noimg.png"

    def get_absolute_url(self):
        return reverse('product_list_by_collection',
                       args=[self.slug])


class Type(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    thumbnail = models.ImageField(
        blank=True,
        default="/media/defaults/noimg.png",
        upload_to='products/types/%Y/%m/%d',
    )

    class Meta:
        ordering = ('name', )
        verbose_name = 'type'
        verbose_name_plural = 'types'

    def __str__(self):
        return self.name

    @property
    def get_thumbnail(self):
        if self.thumbnail:
            return ("https://static.panaya.in/media/" + str(self.thumbnail))
        else:
            return "https://static.panaya.in/media/defaults/noimg.png"

    def get_absolute_url(self):
        return reverse('product_list_by_type',
                       args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.SET_NULL,
        null=True, blank=True)
    collection = models.ForeignKey(
        Collection, related_name='products', on_delete=models.SET_NULL,
        null=True, blank=True)
    type = models.ForeignKey(
        Type, related_name='products', on_delete=models.SET_NULL,
        null=True, blank=True)
    inventory_id = models.CharField(
        max_length=10, db_index=True, unique=True,)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    stocks = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True)
    avg_rating = models.DecimalField(
        default=0,
        max_digits=10,
        decimal_places=2,
        validators=[MaxValueValidator(5), MinValueValidator(0)]
    )
    no_rating = models.PositiveBigIntegerField(default=0)

    class Meta:
        ordering = ('name', )
        index_together = (('id', 'slug'), )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.id, self.slug])

    def get_primary_img(self):
        if self.images.all():
            return self.images.all()[0]
        return "https://static.panaya.in/media/defaults/noimg.png"

    def update_rating(self, new_rating):
        self.avg_rating = ((self.avg_rating*self.no_rating) +
                           new_rating)/(self.no_rating+1)
        self.no_rating = self.no_rating + 1
        self.save()

    def update_stocks(self, quantity):
        quantity = int(quantity)
        if self.stocks < quantity:
            raise ValueError("quantity more than stocks")

        self.stocks = self.stocks-quantity
        if(self.stocks == 0):
            self.available = False
        self.save()

    def realted(self, num_items=3):
        related_category = []
        related_collection = []
        if self.collection:
            related_collection = (
                Collection.objects.get(
                    id=self.collection.id
                ).products.order_by('avg_rating')[:num_items]
            )
        if self.category:
            related_category = (
                Category.objects.get(
                    id=self.category.id
                ).products.order_by('avg_rating')[:num_items]
            )
        related_all = sorted(
            chain(related_collection, related_category), key=lambda obj:
            obj.avg_rating)
        return related_all[:num_items]


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)

    def __str__(self):
        return self.image.url


class Review(models.Model):
    product = models.ForeignKey(
        Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, related_name='reviews', on_delete=models.CASCADE)
    stars = models.IntegerField(default=0)
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return f"{self.stars} stars by {self.user.get_full_name()}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the "real" save() method.
        self.product.update_rating(self.stars)

    def get_rating_stars(self):
        pos_stars = "&#9733;"*self.stars
        neg_stars = "&#9733;"*(5-self.stars)
        return [pos_stars, neg_stars]


class FAQ(models.Model):
    product = models.ForeignKey(
        Product, related_name="faqs", on_delete=models.CASCADE)
    question = models.TextField()
    answer = RichTextField()

    def __str__(self):
        return self.question
