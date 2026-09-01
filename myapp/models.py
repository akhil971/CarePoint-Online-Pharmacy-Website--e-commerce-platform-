from django.db import models

# Create your models here.

class client_message(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    phone_number=models.CharField(max_length=15)
    message=models.TextField() 
    subject=models.CharField() 

    def __str__(self):
        return self.name


class Prescription(models.Model):
    full_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    delivery_address = models.CharField(max_length=255)
    prescription_file = models.FileField(upload_to='prescriptions/')
    additional_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class DoctorAppointment(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    doctor = models.CharField(max_length=100)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    problem_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} with {self.doctor} on {self.appointment_date}"


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('painfever', 'Pain & Fever'),
        ('vitamins', 'Vitamins'),
        ('coldcough', 'Cold & Cough'),
        ('diabetes', 'Diabetes Care'),
        ('firstaid', 'First Aid'),
        ('skincare', 'Skin Care'),
        ('babycare', 'Baby Care'),
        ('devices', 'Devices & Monitors'),
    ]

    TAG_CHOICES = [
        ('OTC', 'OTC'),
        ('Rx', 'Rx (Prescription Required)'),
    ]

    name = models.CharField(max_length=150)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    label = models.CharField(max_length=50, blank=True, help_text="Small text shown above the product name, e.g. PAIN & FEVER")
    description = models.CharField(max_length=255, blank=True, help_text="e.g. 500mg · Strip of 15 Tablets")
    price = models.PositiveIntegerField(help_text="Price in ₹")
    old_price = models.PositiveIntegerField(blank=True, null=True, help_text="Original price in ₹ (optional, shown struck-through)")
    tag = models.CharField(max_length=10, choices=TAG_CHOICES, default='OTC')
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=100)
    is_active = models.BooleanField(default=True, help_text="Uncheck to hide this product from the website")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Wishlist(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='wishlist_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} ❤ {self.product.name}"


class CartItem(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} - {self.product.name} x{self.quantity}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('Placed', 'Placed'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    PAYMENT_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('Online', 'Online Payment'),
    ]

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='orders')
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    delivery_address = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='COD')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Placed')
    total_amount = models.PositiveIntegerField(default=0, help_text="Total order amount in ₹")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.full_name} (₹{self.total_amount})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    product_name = models.CharField(max_length=150, help_text="Product name at the time of order")
    price = models.PositiveIntegerField(help_text="Price per item at the time of order")
    quantity = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product_name} x{self.quantity} (Order #{self.order_id})"