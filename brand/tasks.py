from .services import active_brands, run_campaigns
from .models import Brand
from django_celery_beat.models import PeriodicTask, CrontabSchedule, IntervalSchedule
from celery import shared_task
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)

@shared_task
def campaign_task():
    logger.info("campaign_task started")
    brands = active_brands()
    
    for brand in brands:
        run_campaigns(brand)
        
@shared_task        
def daily_reset():
    logger.info("daily_reset started")
    brands = Brand.objects.filter(daily_limit_reached=True, monthly_limit_reached=False)
    
    for brand in brands:
        brand.daily_limit_reached = False
        brand.save()

@shared_task        
def monthly_reset():
    logger.info("monthly_reset started")
    brands = Brand.objects.filter(monthly_limit_reached=True)
    
    for brand in brands:
        brand.monthly_limit_reached = False
        brand.daily_limit_reached = False
        brand.save()
        
        
def task_create():
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