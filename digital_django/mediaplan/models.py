from django.db import models
from datetime import date
from django.template.defaultfilters import slugify
from random import randint

class Plan(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=100, null=True, blank=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    budget_allocated = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    auto_allocate = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date_modified',)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}/'

    def save(self, *args, **kwargs):
        if not self.id: # create
            if Plan.objects.filter(name=self.name).exists():
                extra = str(randint(1,10000))
                self.slug = slugify(self.name) + '-'+ extra
            else:
                self.slug = slugify(self.name)
        else: # update
            orig = Plan.objects.get(pk=self.id)
            if orig.name != self.name:
                if Plan.objects.filter(name=self.name).exists():
                    extra = str(randint(1,10000))
                    self.slug = slugify(self.name) + '-'+ extra
                else:
                    self.slug = slugify(self.name)
        super(Plan, self).save(*args, **kwargs)

class Phase(models.Model):
    plan = models.ForeignKey(Plan, related_name='phases', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(default=date.today)
    slug = models.SlugField(max_length=100, null=True, blank=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    budget_allocated = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    auto_allocate = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date_added',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.plan.slug}/{self.slug}/'

    def save(self, *args, **kwargs):
        if not self.id: # create
                if Phase.objects.filter(name=self.name).exists():
                    extra = str(randint(1,10000))
                    self.slug = slugify(self.name) + '-'+ extra
                else:
                    self.slug = slugify(self.name)
        else: # update
            orig = Phase.objects.get(pk=self.id)
            if orig.name != self.name:
                if Phase.objects.filter(name=self.name).exists():
                    extra = str(randint(1,10000))
                    self.slug = slugify(self.name) + '-'+ extra
                else:
                    self.slug = slugify(self.name)
        super(Phase, self).save(*args, **kwargs)
        
class Strategy(models.Model):
    phase = models.ForeignKey(Phase, related_name='strategies', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(default=date.today)
    slug = models.SlugField(max_length=100, null=True, blank=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    budget_allocated = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    auto_allocate = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date_added',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.phase.slug}/{self.slug}/'

    def save(self, *args, **kwargs):
        if not self.id: # create
                if Strategy.objects.filter(name=self.name).exists():
                    extra = str(randint(1,10000))
                    self.slug = slugify(self.name) + '-'+ extra
                else:
                    self.slug = slugify(self.name)
        else: # update
            orig = Strategy.objects.get(pk=self.id)
            if orig.name != self.name:
                if Strategy.objects.filter(name=self.name).exists():
                    extra = str(randint(1,10000))
                    self.slug = slugify(self.name) + '-'+ extra
                else:
                    self.slug = slugify(self.name)
        super(Strategy, self).save(*args, **kwargs)

class Country(models.Model):
    strategies = models.ManyToManyField(Strategy, through='TargetCountry', blank=True)
    code = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=100)
    
    class Meta:
        ordering = ('name',)
    
    def __str__(self):
        return self.name

class TargetCountry(models.Model):
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE) 
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    budget_allocated = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    auto_allocate = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

class Channel(models.Model):
    target_countries = models.ManyToManyField(TargetCountry, through='TargetChannel', blank=True)
    code = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=100)
    
    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

class TargetChannel(models.Model):
    target_country = models.ForeignKey(TargetCountry, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    budget_allocated = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    auto_allocate = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

class Device(models.Model):
    target_channels = models.ManyToManyField(TargetChannel, related_name='TargetDevice', blank=True)
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

class TargetDevice(models.Model):
    target_channel = models.ForeignKey(TargetChannel, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    budget_allocated = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    auto_allocate = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

class Ad(models.Model):
    target_devices = models.ManyToManyField(TargetDevice, through='TargetAd', blank=True)
    name = models.CharField(max_length=100)
    
    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

class TargetAd(models.Model):
    target_device = models.ForeignKey(TargetDevice, on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    budget_allocated = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    auto_allocate = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

class Creative(models.Model):
    target_ad = models.ForeignKey(TargetAd, related_name='creatives', blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    budget_allocated = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name 
