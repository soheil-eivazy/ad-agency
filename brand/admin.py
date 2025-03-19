from django.contrib import admin
from .models import Brand, Expense, Campaign



class BrandAdmin(admin.ModelAdmin): 
    list_display = ['title', 'budget_monthly', 'budget_daily', 'monthly_limit_reached', 'daily_limit_reached', 'created_at', 'updated_at']
    
       
class ExpenseAdmin(admin.ModelAdmin): 
    list_display = ['brand_title', 'campaign_title', 'amount', 'created_at']
    
    def brand_title(self, obj):
        return obj.brand.title
    
    def campaign_title(self, obj):
        return obj.campaign.title
    
    
class CampaignAdmin(admin.ModelAdmin):
    list_display = ['title', 'brand_title', 'cost', 'active_from', 'active_to', 'created_at', 'updated_at']

    def brand_title(self, obj):
        return obj.brand.title
    

admin.site.register(Brand, BrandAdmin)
admin.site.register(Campaign, CampaignAdmin)
admin.site.register(Expense, ExpenseAdmin) 