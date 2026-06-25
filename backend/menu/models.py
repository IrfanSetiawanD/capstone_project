from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
import cloudinary.uploader
from cloudinary.models import CloudinaryField


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Menu(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    description = models.TextField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    image = CloudinaryField('image', folder='menus/', null=True, blank=True)

    def __str__(self):
        return self.name


@receiver(post_delete, sender=Menu)
def delete_cloudinary_image_on_delete(sender, instance, **kwargs):
    """
    Satu-satunya tempat yang menghapus file Cloudinary saat object Menu
    dihapus (baik via .delete() instance maupun queryset).
    """
    if instance.image:
        try:
            cloudinary.uploader.destroy(instance.image.public_id)
        except Exception as e:
            print(f"[Cloudinary] Gagal hapus gambar Menu id={instance.pk}: {e}")