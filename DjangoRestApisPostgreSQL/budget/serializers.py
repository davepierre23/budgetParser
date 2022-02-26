from rest_framework import serializers 
from budget.models import Transaction
 
 
class TransactionSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Transaction
        fields = ('id',
                  'title',
                  'description',
                  'published')