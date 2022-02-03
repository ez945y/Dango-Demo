from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15, verbose_name='foneNum')
    address = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class Food(models.Model):
    name = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=3, decimal_places=0)
    comment = models.CharField(max_length=50, blank=True)
    is_spicy = models.BooleanField(default=False)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['price']


class Author(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)


class Comment(models.Model):
    content = models.CharField(max_length=200)
    visitor = models.CharField(max_length=20)
    email = models.EmailField(max_length=20)
    date_time = models.DateTimeField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
