from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)
    class Meta:
        verbose_name_plural = "Categories"
    def __str__(self):
        return self.name

class Menu(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # Menggunakan DecimalField untuk akurasi mata uang
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='menus/', blank=True, null=True)

    def __str__(self):
        return self.name