from django.db import models

# Create your models here.
class Brand(models.Model):
    title = models.CharField(max_length=100)
    budget_monthly = models.FloatField()
    budget_daily = models.FloatField()
    monthly_limit_reached = models.BooleanField(default=False)
    daily_limit_reached = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Campaign(models.Model):
    title = models.CharField(max_length=100)
    brand = models.ForeignKey("brand.Brand", on_delete=models.CASCADE, related_name="campaigns")
    cost = models.FloatField()
    active_from = models.TimeField(null=True, blank=True)
    active_to = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.brand.title}: {self.title}"
    

class Expense(models.Model):
    brand = models.ForeignKey("brand.Brand", on_delete=models.CASCADE)
    campaign = models.ForeignKey("brand.Campaign", on_delete=models.DO_NOTHING, null=True, blank=True)
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.brand.title}: {self.created_at} - {self.amount}"
    
