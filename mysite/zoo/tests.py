from django.test import TestCase
from zoo import models


class AnimalTestCase(TestCase):
    def test_dog_says(self):
        dog = models.Dog(name="Snoopy")
        self.assertEqual(dog.says(), 'woof')

    def test_cat_says(self):
        cat = models.Cat(name="Garfield")
        self.assertEqual(cat.says(), 'meow')


class SimpleTestCase(TestCase):
    fixtures = ['dog.json']

    def test_dog_fixture(self):
        snoopy = Dog.objects.get(id=1)
        self.assertEqual(snoopy.name, 'Snoopy')

# python manage.py dumpdata --indent=4 --format=json zoo.dog >>  fixtures/dog.json
# python manage.py loaddata fixtures/dog.json
