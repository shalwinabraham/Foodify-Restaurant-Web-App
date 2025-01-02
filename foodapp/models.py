from django.db import models
from django.contrib.auth.models import User



class FoodItem(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)
    image = models.ImageField(upload_to='food_images', default='default_image.jpg')

    def __str__(self):
        return self.name


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('user', 'food_item')

    def __str__(self):
        return f"{self.quantity} x {self.food_item.name}"

    def get_total_price(self):
        return self.food_item.price * self.quantity


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    ordered_at = models.DateTimeField(null=True, blank=True) 
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  

    def __str__(self):
        return f"Order Item: {self.food_item.name} in Order #{self.order.id}"


from django.db import models
from django.contrib.auth.models import User

class TableBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    table_number = models.CharField(max_length=10)
    booking_time = models.DateTimeField()
    number_of_guests = models.PositiveIntegerField() 

    def __str__(self):
        return f"Table {self.table_number} booked by {self.user.username} for {self.booking_time} (Guests: {self.number_of_guests})"
