# Django Celery Beat Budget Management System

## 📌 Project Overview
This project automates campaign execution and budget management using **Django**, **Celery**, and **Celery Beat**. It ensures that campaigns run within specified budgets and time constraints (dayparting) while dynamically controlling brand activation status.

## 🚀 How to Run the Project

### **1️⃣ Prerequisites**
Ensure you have the following installed:
- **Docker & Docker Compose**

### **2️⃣ Setup and Start the Services**
1. Clone the repository:
   ```bash
   git clone https://github.com/soheil-eivazy/ad-agency.git
   cd ad-agency
   ```
2. Build and start the services using Docker Compose:
   ```bash
   docker-compose up --build
   ```
3. Run database migrations:
   ```bash
   docker-compose exec ad_agency python manage.py migrate
   ```
4. Run seeder for test data:
   ```bash
   docker-compose exec ad_agency python manage.py seeders
   ```
5. Create a superuser (optional, for Django Admin):
   ```bash
   docker-compose exec ad_agency python manage.py createsuperuser
   ```
6. Access the Django admin panel:
   - **URL:** `http://localhost:8000/admin/`
   - Use the credentials created above.


## 📂 Data Structures

### **1️⃣ Brand Table**
Stores information about brands and their budget limits.
```plaintext
Brand:
    id (Unique Identifier)
    title (String)
    budget_monthly (Float)
    budget_daily (Float)
    monthly_limit_reached (Boolean)
    daily_limit_reached (Boolean)
```

### **2️⃣ Campaign Table**
Manages campaigns linked to brands with time-based constraints.
```plaintext
Campaign:
    id (Unique Identifier)
    brand_id (Foreign Key to Brand)
    title (String)
    cost (Float)
    active_from (Time)  # Dayparting start time
    active_to (Time)  # Dayparting end time
```

### **3️⃣ Expense Table**
Tracks campaign spending per brand and campaign.
```plaintext
Expense:
    id (Unique Identifier)
    brand_id (Foreign Key to Brand)
    campaign_id (Foreign Key to Campaign)
    amount (Float)
    created_at (Datetime)
```

## 🔄 Program Flow

### **1️⃣ Minute-Based Task: Campaign Execution & Budget Check**
- Fetch all **active brands**.
- Fetch **campaigns running at the current time** (dayparting check).
- Check **budget limits** (daily & monthly).
- **Deactivate brands** if budget limits are exceeded.
- Execute campaigns and **log expenses**.

### **2️⃣ Daily Task: Reactivate Brands**
- Check **monthly spending**.
- **Reactivate brands** if the budget still allows for it.

### **3️⃣ Monthly Task: Reset Brands**
- **Reset all brands** to active.

## 🔍 Assumptions & Simplifications
- **Campaigns run only once per matching time slot.**
- **Brands are deactivated immediately upon exceeding budget.**
- **Reactivation happens only daily or monthly, not dynamically.**
- **Dayparting assumes that campaigns cannot run outside their scheduled time.**


