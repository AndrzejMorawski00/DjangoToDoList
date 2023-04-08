from django.db import models
from django.conf import settings
from django.utils.text import slugify
# Create your models here.


class ToDo(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    task_id = models.AutoField(primary_key=True)
    task_name = models.CharField(max_length=50)
    task_details = models.CharField(max_length=200)
    task_important = models.BooleanField(default=False)
    task_deadline = models.DateField(default=None, null=True, blank=True)
    task_slug = models.SlugField(blank=True, default="")
    task_done = models.BooleanField(default=False)
    task_expand = models.BooleanField(default=False)
    task_sorting = models.CharField(default="", max_length=20)
    
    def __str__(self) -> str:
        return f"{self.author} {self.task_name} {self.task_slug}"

    def save(self, *args, **kwargs):
        slug_text = f"{self.task_name} {self.task_id}"
        self.task_slug = slugify(slug_text)
        super(ToDo, self).save(*args, **kwargs)


