from django.core.management.base import BaseCommand
from store.models import Orders, Payment  # Ensure the import matches your app's models

class Command(BaseCommand):
    help = 'Cleanup invalid foreign key references'

    def handle(self, *args, **kwargs):
        # Find invalid orders
        invalid_orders = Orders.objects.exclude(payment_id__in=Payment.objects.values_list('id', flat=True))

        # Delete invalid orders
        deleted_count, _ = invalid_orders.delete()

        self.stdout.write(self.style.SUCCESS(f'Deleted {deleted_count} invalid orders.'))
