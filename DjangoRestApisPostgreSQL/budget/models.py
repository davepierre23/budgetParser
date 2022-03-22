from django.db import models

# Create your models here.



class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    transactonDescript = models.CharField(max_length=500)
    amount = models.FloatField()
    transactonDate =  models.DateField()
    bankAction =models.CharField(max_length=1)
    createdAt = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return self.TransactonDescript


