from django.core.management.base import BaseCommand
from brand.models import Brand, Campaign
from django_celery_beat.models import PeriodicTask, CrontabSchedule, IntervalSchedule

class Command(BaseCommand):
    help = "preparing the database for testing"


    def handle(self, *args, **options):
        schedule, _ = IntervalSchedule.objects.get_or_create(
            every=1,
            period=IntervalSchedule.MINUTES,
        )
        PeriodicTask.objects.get_or_create(
            interval=schedule,  
            name='Campaign Task',
            task='brand.tasks.campaign_task',
        )
        
        schedule, _ = CrontabSchedule.objects.get_or_create(minute=0, hour=0)
        PeriodicTask.objects.get_or_create(
            crontab=schedule,
            name="Daily Budget Reset",
            task="brand.tasks.daily_reset"
        )

        schedule, _ = CrontabSchedule.objects.get_or_create(minute=0, hour=0, day_of_month=1)
        PeriodicTask.objects.get_or_create(
            crontab=schedule,
            name="Monthly Reset",
            task="brand.tasks.monthly_reset"
        )
        
        Brand.objects.get_or_create(
            title="Test Brand",
            budget_monthly=300,
            budget_daily=10
        )
        
        Campaign.objects.get_or_create(
            title="Test Campaign A",
            brand=Brand.objects.first(),
            cost=1
        )
        
        Campaign.objects.get_or_create(
            title="Test Campaign B",
            brand=Brand.objects.first(),
            active_from="10:00:00",
            active_to="11:00:00",
            cost=2
        )
        
        return 