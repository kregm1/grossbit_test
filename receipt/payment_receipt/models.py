from django.db import models


class Item(models.Model):
    title = models.CharField(max_length=255, help_text='Наименование')
    price = models.DecimalField(max_digits=8, decimal_places=2, help_text='стоимость')

    def __str__(self):
        return self.title
