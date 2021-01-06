from celery import shared_task
from rental.apps.properties.models import Reservation


@shared_task
def send_email(reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)
    return