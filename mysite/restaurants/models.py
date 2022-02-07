from django.db import models, connection


class Restaurant(models.Model):
    name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15, verbose_name='foneNum')
    address = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class FoodManager(models.Manager):
    def sfood_order_by_price(self):
        return self.filter(is_spicy=True).order_by('price')

    def sfood(self):
        return self.filter(is_spicy=True)

    def cheap_food_num(self):
        return self.filter(price__lt=100).count()

    def get_120_food(self):
        cursor = connection.cursor()
        cursor.execute("""
            SELECT name
            FROM restaurants_food
            WHERE price=120
        """)
        return [result[0] for result in cursor.fetchall()]


class NotSpicyFoodManager(models.Manager):
    def get_queryset(self):
        return super(NotSpicyFoodManager, self).get_queryset().filter(is_spicy=False)


class SpicyFoodManager(models.Manager):
    def get_queryset(self):
        return super(SpicyFoodManager, self).get_queryset().filter(is_spicy=True)


class Food(models.Model):
    name = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=3, decimal_places=0)
    comment = models.CharField(max_length=50, blank=True)
    is_spicy = models.BooleanField(default=False)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    objects = FoodManager()
    Sobjects = SpicyFoodManager()
    NSobjects = NotSpicyFoodManager()

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

    class Meta:
        ordering = ['date_time']
        permissions = (
            ("can_comment", "Can comment"),
        )


class Account(models.Model):
    money = models.IntegerField()
