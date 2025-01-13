from django.core.management.base import BaseCommand
from api.models import Statistics
import random

class Command(BaseCommand):
    help = 'Populates the statistics collection with sample data'

    def handle(self, *args, **kwargs):
        stats = Statistics.objects.create(
            active_trains=random.randint(30, 50),
            daily_passengers=random.randint(10000, 20000),
            revenue_today=random.uniform(40000, 60000),
            fuel_usage=random.uniform(2000, 3000),
            support_stats={
                'total': random.randint(100, 200),
                'ongoing': random.randint(30, 50),
                'solved': random.randint(70, 100),
                'pending': random.randint(10, 20)
            }
        )
        self.stdout.write(self.style.SUCCESS('Successfully populated statistics')) 