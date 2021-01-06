from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from datetime import timedelta
from django.db.models import Q, Max
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail


class Property(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.FloatField()
    address = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.name

    def available(self):
        max_date = self.reservation_set.annotate(max_end=Max('end')).order_by()
        return max_date + timedelta(days=1)

    def is_occupied(self, start, end):
        now = datetime.now()
        if start and end:
            reservation = self.reservation_set.filter(end__lte=end, start__gte=start)
        else:
            reservation = self.reservation_set.filter(end__lte=now, start__gte=now)

        if reservation.exist():
            return True
        else:
            return False


class Reservation(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.DO_NOTHING)
    payment_method = models.ForeignKey('properties.PaymentMethod', on_delete=models.DO_NOTHING)
    start = models.DateField()
    end = models.DateField()

    def __str__(self):
        return f'{self.property.name} - ({self.start} - {self.end})'

    def calculate_price(self):
        delta = self.end - self.start
        total = self.property.price * delta.days
        return total


class Image(models.Model):
    name = models.CharField(max_length=255)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    default = models.BooleanField(default=False)


class PaymentMethod(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


@receiver(post_save, sender=Reservation)
def send_email(sender, instance, **kwargs):
    send_mail(
        f'Reservation {instance.id}',
        f'Hi, {instance.user.name}',
        'from@hello.com',
        [instance.customer.email, instance.property.owner.email],
        fail_silently=False,
    )


