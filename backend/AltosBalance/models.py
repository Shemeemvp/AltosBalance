from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('company', 'Company'),
        ('distributor', 'Distributor'),
        ('staff', 'Staff'),
        ('superuser', 'Superuser'),
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
