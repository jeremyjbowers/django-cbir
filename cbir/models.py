from django.db import models

class Year(models.Model):
    year = models.IntegerField(max_length=4)
    
    def __unicode__(self):
        return u'%s' % self.year

class Lawmaker(models.Model):
    dirty_name = models.CharField(max_length=255)
    clean_name = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField()
    
    def __unicode__(self):
        if self.clean_name != None or self.clean_name != '':
            return self.clean_name
        else:
            return self.dirty_name
    
    def save(self, *args, **kwargs):
        if self.slug == None or self.slug == '':
            self.slug = slugify(self.__unicode__())
        super(Series, self).save(*args, **kwargs)
    
class Earmark(models.Model):
    line_number = models.IntegerField(default=0, max_length=10)
    tracking_number = models.IntegerField(default=0, max_length=10)
    title = models.CharField(max_length=255)
    detail_url = models.CharField(max_length=255)
    amount = models.IntegerField(default=0, max_length=15)
    lawmaker = models.ForeignKey(Lawmaker)
    year = models.ForeignKey(Year)
    
    def __unicode__(self):
        return u'%s: %s' % (self.year.year, self.title)