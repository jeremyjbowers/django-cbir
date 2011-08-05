from django.db import models
from django.db.models import Count, Aggregate, Sum
from django.template.defaultfilters import slugify

class Year(models.Model):
    year = models.IntegerField(max_length=4)
    
    def __unicode__(self):
        return u'%s' % self.year
    
    def get_base_url(self):
        return u'http://www.myfloridahouse.gov/FileStores/Adhoc/Appropriations/CBIRS/cbirs-house%s/' % self.year
    
    def get_earmark_url(self):
        return u'%sWebList.htm' % self.get_base_url()
    

class Lawmaker(models.Model):
    dirty_name = models.CharField(max_length=255)
    clean_name = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField()
    amount_2008 = models.IntegerField(default=0, max_length=100, null=True)
    amount_2007 = models.IntegerField(default=0, max_length=100, null=True)
    amount_2006 = models.IntegerField(default=0, max_length=100, null=True)
    amount_2005 = models.IntegerField(default=0, max_length=100, null=True)
    amount_2004 = models.IntegerField(default=0, max_length=100, null=True)
    amount_2003 = models.IntegerField(default=0, max_length=100, null=True)
    
    def __unicode__(self):
        return self.dirty_name
    
    def save(self, *args, **kwargs):
        if self.slug == None or self.slug == '':
            self.slug = slugify(self.__unicode__())
        self.amount_2008 = self.get_earmark_sum_2008()
        self.amount_2007 = self.get_earmark_sum_2007()
        self.amount_2006 = self.get_earmark_sum_2006()
        self.amount_2005 = self.get_earmark_sum_2005()
        self.amount_2004 = self.get_earmark_sum_2004()
        self.amount_2003 = self.get_earmark_sum_2003()
        super(Lawmaker, self).save(*args, **kwargs)
    
    def get_earmark_sums(self):
        return Earmark.objects.filter(lawmaker=self).values('year__year').annotate(Sum('amount')).order_by('-amount__sum')
    
    def get_earmark_counts(self):
        return Earmark.objects.filter(lawmaker=self).values('year__year').annotate(Count('year')).order_by('-year__count')
    
    def get_earmark_sum_2008(self):
        year = Year.objects.get(year=2008)
        return Earmark.objects.filter(lawmaker=self, year=year).aggregate(Sum('amount'))['amount__sum']
        
    def get_earmark_sum_2007(self):
        year = Year.objects.get(year=2007)
        return Earmark.objects.filter(lawmaker=self, year=year).aggregate(Sum('amount'))['amount__sum']
        
    def get_earmark_sum_2006(self):
        year = Year.objects.get(year=2006)
        return Earmark.objects.filter(lawmaker=self, year=year).aggregate(Sum('amount'))['amount__sum']
        
    def get_earmark_sum_2005(self):
        year = Year.objects.get(year=2005)
        return Earmark.objects.filter(lawmaker=self, year=year).aggregate(Sum('amount'))['amount__sum']
        
    def get_earmark_sum_2004(self):
        year = Year.objects.get(year=2004)
        return Earmark.objects.filter(lawmaker=self, year=year).aggregate(Sum('amount'))['amount__sum']

    def get_earmark_sum_2003(self):
        year = Year.objects.get(year=2003)
        return Earmark.objects.filter(lawmaker=self, year=year).aggregate(Sum('amount'))['amount__sum']
        
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