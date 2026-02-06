from django.db import models


PROPERTY_TYPES = (
    ('Villa', 'Villa'),
    ('Apartment', 'Apartment'),
    ('House', 'House'),
    ('Land', 'Land'),
)

class Property(models.Model):
    title = models.CharField(max_length=200)
    price = models.CharField(max_length=50)
    location = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=PROPERTY_TYPES, default='Villa')
    bedrooms = models.IntegerField(null=True, blank=True)
    area = models.CharField(max_length=50, null=True, blank=True)
    lat = models.FloatField(default=0.0)
    lng = models.FloatField(default=0.0)
    image = models.ImageField(upload_to='properties/', null=True, blank=True)

    def __str__(self):
        return self.title

class Register(models.Model):
    fname = models.CharField(max_length=50)
    mobile = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255) 
    def __str__(self):
        return self.email


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Enquiry(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    message = models.TextField(blank=True)
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="enquiries"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.property.title}"

class Cart(models.Model):
    user = models.ForeignKey(
        Register,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "property")

    def __str__(self):
        return f"{self.user.email} - {self.property.title}"


