from django.db import models

# Create your models here.



class Transaction(models.Model):
    Id = models.AutoField(primary_key=True)
    TransactonDescript = models.CharField(max_length=500)
    Amount = models.IntegerField()
    TransactonDate =  models.DateField()
    BankAction =models.CharField(max_length=1)

    def __str__(self) -> str:
        return self.TransactonDescript
    
