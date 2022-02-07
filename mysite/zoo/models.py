from django.db import models


class Animal(models.Model):
    name = models.CharField(max_length=256)

    def says(self):
        raise NotImplementedError("I don't know what to do")

    class Meta:
        abstract = True


class Dog(Animal):

    def says(self):
        return "woof"


class Cat(Animal):

    def says(self):
        return "meow"
