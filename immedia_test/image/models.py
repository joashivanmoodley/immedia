from django.db import models

'''
DB Model definition for Django ORM to control DB.
'''


class Location(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    cc = models.CharField(max_length=5, db_index=True)
    country = models.CharField(max_length=50, blank=True, db_index=True)
    province = models.CharField(max_length=50, db_index=True)
    region = models.CharField(max_length=50, db_index=True)
    latitude = models.CharField(max_length=50, null=True, blank=True)
    longitude = models.CharField(max_length=50, null=True, blank=True)

    def __unicode__(self):
        return "%s, %s, %s" % (
            self.country, self.province, self.region,)

    class Meta:
        app_label = 'image'
        unique_together = (
            'country',
            'province',
            'region',
        )


class LandMark(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    location = models.ForeignKey(Location, blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    latitude = models.CharField(max_length=50, null=True, blank=True)
    longitude = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)

    def __unicode__(self):
        return "%s" % (self.name)

    class Meta:
        app_label = 'image'


class Image(models.Model):
    date_added = models.DateTimeField(blank=True, null=True)
    land_mark = models.ForeignKey(LandMark, blank=True, null=True)
    image = models.URLField(max_length=250)
    image_type = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    owner = models.CharField(max_length=150, blank=True, null=True)

    def __unicode__(self):
        return "%s" % (self.image)

    class Meta:
        app_label = 'image'
        ordering = ['id']
