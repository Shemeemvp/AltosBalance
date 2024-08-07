from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    ROLE_CHOICES = [
        ('Company', 'Company'),
        ('Distributor', 'Distributor'),
        ('Staff', 'Staff')
    ]
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='altos_balance_user_set',  # Add this line to avoid conflict
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='altos_balance_user_permissions',  # Add this line to avoid conflict
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username


class PaymentTerms(models.Model):
    payment_terms_number = models.IntegerField(null=True, blank=True)
    payment_terms_value = models.CharField(max_length=100, null=True, blank=True)
    days = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.payment_terms_value} ({self.days} days)"


class Distributor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    payment_term = models.ForeignKey(
        PaymentTerms, on_delete=models.SET_NULL, null=True, blank=True
    )
    distributor_code = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    contact = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to="image/distributor")
    start_date = models.DateField(auto_now_add=True, null=True)
    end_date = models.DateField(null=True, blank=True)
    admin_approval_status = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    distributor = models.ForeignKey(
        Distributor, on_delete=models.SET_NULL, null=True, blank=True
    )
    payment_term = models.ForeignKey(
        PaymentTerms, on_delete=models.SET_NULL, null=True, blank=True
    )
    company_name = models.CharField(max_length=255, null=True, blank=True)
    business_name = models.CharField(max_length=255, null=True, blank=True)
    industry = models.CharField(max_length=255, null=True, blank=True)
    company_type = models.CharField(max_length=255, null=True, blank=True)
    company_code = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    contact = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    pincode = models.IntegerField(null=True, blank=True)
    pan_no = models.CharField(max_length=255, null=True, blank=True)
    gst_type = models.CharField(max_length=255, null=True, blank=True)
    gst_no = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to="image/company")
    start_date = models.DateField(auto_now_add=True, null=True)
    end_date = models.DateField(null=True, blank=True)
    payment_type = models.CharField(max_length=255, null=True, blank=True)
    accountant = models.CharField(max_length=255, null=True, blank=True)
    admin_approval_status = models.CharField(max_length=255, null=True, blank=True)
    distributor_approval_status = models.CharField(
        max_length=255, null=True, blank=True
    )
    registration_type = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.company_name


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    contact = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to="image/staff")
    company_approval_status = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class TrialPeriod(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    interested_in_buying = models.IntegerField(default=0)
    feedback = models.TextField(blank=True, null=True)

    def is_active(self):
        return self.end_date >= timezone.now().date()
    
class Modules_List(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE,null=True,blank=True)

    # -----items-----
    Items = models.IntegerField(null=True,default=0) 
    Price_List = models.IntegerField(null=True,default=0) 
    Stock_Adjustment = models.IntegerField(null=True,default=0) 

    # --------- CASH & BANK-----
    Cash_in_hand = models.IntegerField(null=True,default=0) 
    Offline_Banking = models.IntegerField(null=True,default=0)
    Bank_Reconciliation = models.IntegerField(null=True,default=0)
    UPI = models.IntegerField(null=True,default=0)
    Bank_Holders = models.IntegerField(null=True,default=0)
    Cheque = models.IntegerField(null=True,default=0)
    Loan_Account = models.IntegerField(null=True,default=0)

    #  ------SALES MODULE -------
    Customers  = models.IntegerField(null=True,default=0)
    Invoice = models.IntegerField(null=True,default=0) 
    Estimate = models.IntegerField(null=True,default=0) 
    Sales_Order = models.IntegerField(null=True,default=0) 
    Recurring_Invoice = models.IntegerField(null=True,default=0) 
    Retainer_Invoice = models.IntegerField(null=True,default=0) 
    Credit_Note = models.IntegerField(null=True,default=0) 
    Payment_Received = models.IntegerField(null=True,default=0) 
    Delivery_Challan = models.IntegerField(null=True,default=0)

    #  ---------PURCHASE MODULE--------- 
    Vendors = models.IntegerField(null=True,default=0) 
    Bills = models.IntegerField(null=True,default=0) 
    Recurring_Bills = models.IntegerField(null=True,default=0) 
    Debit_Note = models.IntegerField(null=True,default=0) 
    Purchase_Order = models.IntegerField(null=True,default=0) 
    Expenses = models.IntegerField(null=True,default=0) 
    Recurring_Expenses = models.IntegerField(null=True,default=0) 
    Payment_Made = models.IntegerField(null=True,default=0) 

    # --------EWay_Bill-----
    EWay_Bill = models.IntegerField(null=True,default=0) 

    #  -------ACCOUNTS--------- 
    Chart_of_Accounts = models.IntegerField(null=True,default=0)  
    Manual_Journal = models.IntegerField(null=True,default=0)  
    Reconcile = models.IntegerField(null=True,default=0) 

    # -------PAYROLL------- 
    Employees = models.IntegerField(null=True,default=0) 
    Employees_Loan = models.IntegerField(null=True,default=0)  
    Holiday = models.IntegerField(null=True,default=0) 
    Attendance = models.IntegerField(null=True,default=0) 
    Salary_Details = models.IntegerField(null=True,default=0) 

    update_action = models.IntegerField(null=True,default=0) 
    status = models.CharField(max_length=100,null=True,default='New')

class Units(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=100,null=True)

class Loan_Term(models.Model):
    duration= models.IntegerField(null=True,blank=True)
    term = models.CharField(max_length=255,null=True,blank=True)
    days = models.IntegerField(null=True,blank=True)
    company = models.ForeignKey(Company,on_delete=models.CASCADE,null=True,blank=True)

class Company_Payment_Terms(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    term_name = models.CharField(max_length=100, null=True)
    days = models.IntegerField(null=True, default=0)

class CompanyRepeatEvery(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE,null=True,blank=True)
    repeat_every = models.CharField(max_length=100,null=True,blank=True) 
    repeat_type = models.CharField(max_length=100,null=True,blank=True) 
    duration = models.IntegerField(null=True,blank=True)
    days = models.IntegerField(null=True,blank=True)


class Chart_Of_Account(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    account_type = models.CharField(max_length=255,null=True,blank=True)
    account_name = models.CharField(max_length=255,null=True,blank=True)
    account_code = models.CharField(max_length=255,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    balance = models.FloatField(null=True, blank=True, default=0.0)
    balance_type = models.CharField(max_length=100,null=True,blank=True)
    credit_card_no = models.CharField(max_length=255,null=True,blank=True)
    sub_account = models.BooleanField(null=True,blank=True, default=False)
    parent_account = models.CharField(max_length=255,null=True,blank=True)
    bank_account_no = models.BigIntegerField(null=True,blank=True)
    date = models.DateField(auto_now_add=True, auto_now=False, null=True, blank=True)
    create_status=models.CharField(max_length=255,null=True,blank=True)
    status = models.CharField(max_length=255,null=True,blank=True)

class ChartOfAccount_History(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    account = models.ForeignKey(Chart_Of_Account, on_delete=models.CASCADE, null=True)
    date = models.DateField(auto_now_add=True, auto_now=False, null=True)
    action_choices = [
        ('Created', 'Created'),
        ('Edited', 'Edited'),
    ]
    action = models.CharField(max_length=20, null=True, blank = True, choices=action_choices)

class Eway_Transportation(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True) 
    Name = models.CharField(max_length=200, null= True)
    Type = models.CharField(max_length=100, null=True)


class Stock_Reason(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE,null=True,blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    reason = models.CharField(max_length=500)

class Payment_Terms_updation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    payment_term = models.ForeignKey(PaymentTerms, on_delete=models.CASCADE,null=True,blank=True)
    status = models.CharField(max_length=100,null=True,default='New')

class CNotification(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE,null=True,blank=True)
    # item = models.ForeignKey(Items, on_delete = models.CASCADE, null=True, blank=True)
    # customers = models.ForeignKey(Customers, on_delete = models.CASCADE, null=True,blank=True)
    # vendors = models.ForeignKey(Fin_Vendors, on_delete = models.CASCADE, null=True,blank=True)
    
    title = models.CharField(max_length=255,null=True,blank=True)
    description = models.CharField(max_length=255,null=True,blank=True) 
    noti_date = models.DateTimeField(auto_now_add=True,null=True)
    date_created = models.DateField(auto_now_add=True,null=True)
    time=models.TimeField(auto_now_add=True,null=True)
    status = models.CharField(max_length=100,null=True,default='New')


class ANotification(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    module_list = models.ForeignKey(Modules_List, on_delete=models.CASCADE,null=True,blank=True)
    payment_terms_updation = models.ForeignKey(Payment_Terms_updation, on_delete=models.CASCADE,null=True,blank=True)
    
    title = models.CharField(max_length=255,null=True,blank=True)
    description = models.CharField(max_length=255,null=True,blank=True) 
    noti_date = models.DateTimeField(auto_now_add=True,null=True)
    date_created = models.DateField(auto_now_add=True,null=True)
    time=models.TimeField(auto_now_add=True,null=True)
    status = models.CharField(max_length=100,null=True,default='New')  

class DNotification(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    distributor = models.ForeignKey(Distributor, on_delete=models.CASCADE,null=True,blank=True)
    module_list = models.ForeignKey(Modules_List, on_delete=models.CASCADE,null=True,blank=True)
    payment_terms_updation = models.ForeignKey(Payment_Terms_updation, on_delete=models.CASCADE,null=True,blank=True)
    
    title = models.CharField(max_length=255,null=True,blank=True)
    description = models.CharField(max_length=255,null=True,blank=True) 
    noti_date = models.DateTimeField(auto_now_add=True,null=True)
    date_created = models.DateField(auto_now_add=True,null=True)
    time=models.TimeField(auto_now_add=True,null=True)
    status = models.CharField(max_length=100,null=True,default='New')