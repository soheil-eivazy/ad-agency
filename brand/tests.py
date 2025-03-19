from django.test import TestCase
from .models import Brand, Expense, Campaign
from .services import spend, monthly_limit_reached, daily_limit_reached, outside_time_limit, limit_reached, active_brands, run_campaigns
from datetime import datetime, timedelta

class SpendServiceTests(TestCase):

    def setUp(self):
        self.brand = Brand.objects.create(
            title="Test Brand",
            budget_monthly=10000,
            budget_daily=500
        )
        self.campaign = Campaign.objects.create(
            title="Test Campaign",
            brand=self.brand,
            cost=100
        )

    def test_spend_within_limits(self):
        result = spend(self.brand, self.campaign)
        self.assertIsNotNone(result)
        self.assertEqual(result.amount, 100)
        self.assertEqual(result.brand, self.brand)
        self.assertEqual(result.campaign, self.campaign)

    def test_monthly_limit_reached(self):
        self.campaign.cost = 550
        for _ in range(20):
            spend(self.brand, self.campaign)
        result = monthly_limit_reached(self.brand, self.campaign.cost)
        self.assertTrue(result)

    def test_daily_limit_reached(self):
        spend(self.brand, self.campaign)
        self.campaign.cost = 550
        result = daily_limit_reached(self.brand, self.campaign.cost)
        self.assertTrue(result)

    def test_outside_time_limit(self):
        self.campaign.active_from = datetime.now().time()
        self.campaign.active_to = (datetime.now() + timedelta(hours=1)).time()
        self.campaign.save()
        result = outside_time_limit(self.campaign)
        self.assertFalse(result)

    def test_limit_reached(self):
        for _ in range(20):
            spend(self.brand, self.campaign)
        result = limit_reached(self.brand, 200)
        self.assertTrue(result)

    def test_active_brands(self):
        brands = active_brands()
        self.assertIn(self.brand, brands)

    def test_run_campaigns(self):
        run_campaigns(self.brand)
        self.assertEqual(Expense.objects.count(), 1)
        self.assertEqual(Expense.objects.first().amount, 100)