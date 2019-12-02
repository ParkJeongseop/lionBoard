from django.db import models

# Create your models here.

# Create your models here.
class Blog(models.Model):
     title = models.CharField(max_length = 200)
     date = models.DateTimeField(auto_now=True)
     body = models.TextField()
     img = models.ImageField(blank=True, null=True)
     img2 = models.ImageField(upload_to="image2", blank=True, null=True)

     def __str__(self):
         return self.title

     def summary(self):
        return self.body[:100]


