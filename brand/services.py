from .models import Brand, Expense, Campaign
from datetime import datetime
from django.db.models import Sum, Q


def spend(brand: Brand, campaign: Campaign) -> Expense:  
    expense = Expense(amount=campaign.cost, brand=brand, campaign=campaign)
    expense.save()
    return expense


def monthly_limit_reached(brand: Brand, amount: float) -> bool:
    monthly_amount = Expense.objects.filter(created_at__month=datetime.now().month, brand=brand).aggregate(Sum('amount'))['amount__sum']
    print("monthly_amount", monthly_amount)
    monthly_amount = monthly_amount if monthly_amount is not None else 0.0
    return amount + monthly_amount > brand.budget_monthly


def daily_limit_reached(brand: Brand, amount: float) -> bool:
    daily_amount = Expense.objects.filter(created_at__day=datetime.now().day, brand=brand).aggregate(Sum('amount'))['amount__sum']
    print("daily_amount", daily_amount)
    daily_amount = daily_amount if daily_amount is not None else 0.0
    return amount + daily_amount > brand.budget_daily
    
    

def outside_time_limit(campaign: Campaign) -> bool:
    if campaign.active_from is None or campaign.active_to is None:
        return False
    
    return campaign.active_from >= datetime.now().time() or campaign.active_to <= datetime.now().time()


def limit_reached(brand: Brand, amount: float) -> bool:
    if monthly_limit_reached(brand, amount):
        brand.monthly_limit_reached = True
        brand.save()
        return True
    
    if daily_limit_reached(brand, amount):
        brand.daily_limit_reached = True
        brand.save()
        return True
    
    return False


def active_brands() -> list[Brand]:
    brands = Brand.objects.filter(
        monthly_limit_reached=False, 
        daily_limit_reached=False
    )
    
    return brands


def run_campaigns(brand: Brand):
    now = datetime.now().time()
    campaigns = Campaign.objects.filter(brand=brand).filter(
        Q(active_from__isnull=True) | Q(active_from__lte=now),
        Q(active_to__isnull=True) | Q(active_to__gte=now)
    )
    
    for campaign in campaigns:
        if limit_reached(brand, campaign.cost):
            print(f"Skipping campaign {campaign.title} due to budget limits")
            break
        
        result = spend(brand, campaign)
        print(f"Successfully ran campaign {campaign.title} with expense {result.amount}")