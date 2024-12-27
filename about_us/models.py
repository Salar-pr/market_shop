from django.db import models

class AboutUs(models.Model):
  title = models.CharField(max_length=50)
  text = models.TextField()
  img = models.ImageField(upload_to="about_us",width_field=100,height_field=150,null=True,blank=True)

  class Meta:
        verbose_name = "AboutUS"
        verbose_name_plural = "درباره ما"