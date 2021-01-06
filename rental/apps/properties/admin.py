from django.contrib import admin

from .models import Property, Reservation, Image, PaymentMethod


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'name', 'price', 'address', 'description')
    list_filter = ('owner',)
    search_fields = ('name',)


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer',
        'property',
        'payment_method',
        'start',
        'end',
    )
    list_filter = ('customer', 'property', 'payment_method', 'start', 'end')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'property', 'image', 'default')
    list_filter = ('property', 'default')
    search_fields = ('name',)


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)