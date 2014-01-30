from django.db import models


class Picture(models.Model):
    class Meta:
        verbose_name = 'Picture'
        verbose_name_plural = 'Pictures'

    def __unicode__(self):
        return self.title or self.file

    title = models.CharField('Title', max_length=80, blank=True, null=True)
    file = models.ImageField('Image', upload_to='uploads/')
