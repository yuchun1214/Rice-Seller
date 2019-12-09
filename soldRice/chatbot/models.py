from django.db import models

class Customer(models.Model):
    user_name = models.CharField(max_length=30,default='')
    user_id = models.CharField(max_length=50,default='')
    PRODUCTS = [
        ('WR', 'White Rice'),
        ('BR', 'Brown Rice'),
    ]
    products = models.CharField(max_length=5, choices=PRODUCTS,null=True)
    amount = models.IntegerField(default=0)
    receiver = models.CharField(max_length=30,null=True)
    address = models.CharField(max_length=50,null=True)
    state = models.CharField(max_length=20, default="user")
    user_confirm = models.BooleanField(default=False)
    
    pass

# Create your models here.
