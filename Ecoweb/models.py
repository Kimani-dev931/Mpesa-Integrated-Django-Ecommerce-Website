from django.conf import settings
from django.db import models
from django.shortcuts import reverse

SHOE_SIZES = (
    ('seven', '7'),
    ('eight', '8'),
    ('nine', '9'),
    ('ten', '10'),
    ('eleven', '11'),
    ('twelve', '12'),
    ('thirteen', '13'),
    ('fourteen', '14'),

)


class Item(models.Model):
    title = models.CharField(max_length=200)
    price = models.FloatField()
    photo = models.ImageField(upload_to='pics')
    shoe_size = models.CharField(choices=SHOE_SIZES, max_length=15, null=True)
    slug = models.SlugField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("detail", kwargs={'slug': self.slug})

    def get_add_cart_url(self):
        return reverse("add-to-cart", kwargs={'slug': self.slug})

    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={'slug': self.slug})


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        return total
