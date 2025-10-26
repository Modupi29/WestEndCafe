from django.db import models
from django.contrib.auth.models import User
from menu.models import MenuItem
from django.conf import settings

# Create your models here.

class Order(models.Model):
    PAYMENT_CHOICES = [
        ('Pay Now', 'Pay Now'),
        ('Pay in Store', 'Pay in Store'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(MenuItem, through='OrderItem')
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    payment_option = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    proof = models.FileField(upload_to='proofs/', blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='cart_orderitems')
    quantity = models.PositiveIntegerField(default=1)

    def get_total(self):
        return self.item.price * self.quantity
    
    def __str__(self):
        return f"{self.quantity} x {self.item.name} in Order #{self.order.id}"