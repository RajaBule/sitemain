from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Samples(models.Model):
    id = models.CharField(max_length=300, primary_key=True)
    name = models.CharField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=3)
    stype = models.CharField(max_length=300, null=True)
    project = models.CharField(max_length=300, null=True, blank=True)
    location = models.CharField(max_length=300, null=True)
    proccessing = models.CharField(max_length=300, null=True)
    cropyear = models.CharField(max_length=300, null=True)
    varieties = models.CharField(max_length=300, null=True)
    regdate = models.CharField(max_length=300, null=True, blank=True)
    grade = models.CharField(max_length=300, null=True, blank=True)
    rating = models.CharField(max_length=300, null=True, blank=True)
    cert = models.CharField(max_length=300, null=True, blank=True)
    notes = models.TextField(max_length=300, null=True, blank=True)
    refid = models.CharField(max_length=300, null=True, blank=True)
    salenum = models.CharField(max_length=300, null=True, blank=True)
    iconum = models.CharField(max_length=300, null=True, blank=True)
    contnum = models.CharField(max_length=300, null=True, blank=True)
    tracknum = models.CharField(max_length=300, null=True, blank=True)
    country = models.CharField(max_length=300, null=True, blank=True)
    farm = models.CharField(max_length=300, null=True, blank=True)
    importer = models.CharField(max_length=300, null=True, blank=True)
    exporter = models.CharField(max_length=300, null=True, blank=True)
    wetmill = models.CharField(max_length=300, null=True, blank=True)
    drymill = models.CharField(max_length=300, null=True, blank=True)
    cooperative = models.CharField(max_length=300, null=True, blank=True)
    assosiation = models.CharField(max_length=300, null=True, blank=True)
    customer = models.CharField(max_length=300, null=True, blank=True)
    othertrac = models.TextField(max_length=300, null=True, blank=True)
    sampleweight = models.CharField(max_length=300, null=True, blank=True)
    sampleweightunit = models.CharField(max_length=300, null=True, blank=True)
    expweight = models.CharField(max_length=300, null=True, blank=True)
    expweightunit = models.CharField(max_length=300, null=True, blank=True)
    expprice = models.CharField(max_length=300, null=True, blank=True)
    exptotalprice = models.CharField(max_length=300, null=True, blank=True)
    exparrival = models.CharField(max_length=300, null=True, blank=True)
    moisture = models.CharField(max_length=300, null=True, blank=True)
    wa = models.CharField(max_length=300, null=True, blank=True)
    density = models.CharField(max_length=300, null=True, blank=True)
    physicaldefects = models.CharField(max_length=300, null=True)
    screensize = models.CharField(max_length=300, null=True, blank=True)
    classification = models.CharField(max_length=300, null=True, blank=True)
    estgreenweight = models.CharField(max_length=300, null=True, blank=True)
    sensorialdescriptors = models.TextField(max_length=300, null=True, blank=True)
    generalcomments = models.TextField(max_length=300, null=True, blank=True)
    sensorial = models.CharField(max_length=300, null=True, blank=True)
    shared_with = models.ManyToManyField(User, through='SampleShare', related_name='shared_samples', blank=True)
    view_perms = models.ManyToManyField(User, through='ViewPerms', related_name='sample_view_perms', blank=True)
    def __str__(self):
        return self.id
    
class ViewPerms(models.Model):
    #id = models.CharField(max_length=300, primary_key=True)
    sample = models.ForeignKey(Samples, on_delete=models.CASCADE)
    name = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stype = models.BooleanField(default=False)
    project = models.BooleanField(default=False)
    location = models.BooleanField(default=True)
    proccessing = models.BooleanField(default=True)
    cropyear = models.BooleanField(default=True)
    varieties = models.BooleanField(default=True)
    regdate = models.BooleanField(default=True)
    grade = models.BooleanField(default=True)
    rating = models.BooleanField(default=False)
    cert = models.BooleanField(default=False)
    notes = models.BooleanField(default=False)
    refid = models.BooleanField(default=False)
    salenum = models.BooleanField(default=False)
    iconum = models.BooleanField(default=False)
    contnum = models.BooleanField(default=False)
    tracknum = models.BooleanField(default=False)
    country = models.BooleanField(default=True)
    farm = models.BooleanField(default=False)
    importer = models.BooleanField(default=False)
    exporter = models.BooleanField(default=False)
    wetmill = models.BooleanField(default=False)
    drymill = models.BooleanField(default=False)
    cooperative = models.BooleanField(default=False)
    assosiation = models.BooleanField(default=False)
    customer = models.BooleanField(default=False)
    othertrac = models.BooleanField(default=False)
    sampleweight = models.BooleanField(default=False)
    sampleweightunit = models.BooleanField(default=False)
    expweight = models.BooleanField(default=False)
    expweightunit = models.BooleanField(default=False)
    expprice = models.BooleanField(default=False)
    exptotalprice = models.BooleanField(default=False)
    exparrival = models.BooleanField(default=False)
    moisture = models.BooleanField(default=True)
    wa = models.BooleanField(default=True)
    density = models.BooleanField(default=True)
    physicaldefects = models.BooleanField(default=True)
    screensize = models.BooleanField(default=True)
    classification = models.BooleanField(default=False)
    estgreenweight = models.BooleanField(default=False)
    sensorialdescriptors = models.BooleanField(default=True)
    generalcomments = models.BooleanField(default=False)
    sensorial = models.BooleanField(default=True)
    can_share = models.BooleanField(default=False)
    
    def __str__(self):
        return self.id
    
class SampleShare(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sample = models.ForeignKey(Samples, on_delete=models.CASCADE)
    can_alter = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sample} shared with {self.user}"
    

class CuppingSCI(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=3)
    sample_id = models.CharField(max_length=10000)
    roast_level_range = models.FloatField(null=True, blank=True, default=0)
    ferment_level_range = models.FloatField(null=True, blank=True, default=0)
    fragrance_range = models.FloatField(null=True, blank=True, default=0)
    fragrance_intensity_range = models.FloatField(null=True, blank=True, default=0)
    fragrance_notes = models.TextField(null=True, blank=True)
    flavor_range = models.FloatField(null=True, blank=True, default=0)
    flavor_intensity_range = models.FloatField(null=True, blank=True, default=0)
    Flavor_notes = models.TextField(null=True, blank=True)
    aroma_range = models.FloatField(null=True, blank=True, default=0)
    aroma_intensity_range = models.FloatField(null=True, blank=True, default=0)
    aroma_notes = models.TextField(null=True, blank=True)
    acidity_range = models.FloatField(null=True, blank=True, default=0)
    acidity_intensity_range = models.FloatField(null=True, blank=True, default=0)
    Acidity_notes = models.TextField(null=True, blank=True)
    body_range = models.FloatField(null=True, blank=True, default=0)
    body_thickness_range = models.FloatField(null=True, blank=True, default=0)
    body_notes = models.TextField(null=True, blank=True)
    sweetness_range = models.FloatField(null=True, blank=True, default=0)
    sweetness_intensity_range = models.FloatField(null=True, blank=True, default=0)
    sweetness_notes = models.TextField(null=True, blank=True)
    aftertaste_range = models.FloatField(null=True, blank=True, default=0)
    aftertaste_duration_range = models.FloatField(null=True, blank=True, default=0)
    aftertaste_notes = models.TextField(null=True, blank=True)
    fresh_range = models.FloatField(null=True, blank=True, default=0)
    fresh_woody_range = models.FloatField(null=True, blank=True, default=0)
    freshcrop_notes = models.TextField(null=True, blank=True, default=0)
    off_1_range = models.IntegerField(null=True, blank=True, default=0)
    off_2_range = models.IntegerField(null=True, blank=True, default=0)
    off_3_range = models.IntegerField(null=True, blank=True, default=0)
    off_4_range = models.IntegerField(null=True, blank=True, default=0)
    off_5_range = models.IntegerField(null=True, blank=True, default=0)
    off_notes = models.TextField(null=True, blank=True)
    uniform_1_range = models.IntegerField(null=True, blank=True, default=0)
    uniform_2_range = models.IntegerField(null=True, blank=True, default=0)
    uniform_3_range = models.IntegerField(null=True, blank=True, default=0)
    uniform_4_range = models.IntegerField(null=True, blank=True, default=0)
    uniform_5_range = models.IntegerField(null=True, blank=True, default=0)
    uniformity_notes = models.TextField(null=True, blank=True)
    sens_descriptors = models.TextField(null=True, blank=True)
    total_cup_score = models.TextField(null=True, blank=True)
    cupdate = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.sample_id
    
class Inventory(models.Model):
    id = models.CharField(max_length=300, primary_key=True)
    sampleid = models.CharField(max_length=300, null=True, blank=True)
    code = models.CharField(max_length=300, null=True, blank=True)
    pricelocal = models.CharField(max_length=300, null=True, blank=True)
    priceexport = models.CharField(max_length=300, null=True, blank=True)
    name = models.CharField(max_length=300)
    totalq = models.CharField(max_length=300, null=True, blank=True)
    g1q = models.CharField(max_length=300, null=True, blank=True)
    g2q = models.CharField(max_length=300, null=True, blank=True)
    g3q = models.CharField(max_length=300, null=True, blank=True)
    g4q = models.CharField(max_length=300, null=True, blank=True)
    g5q = models.CharField(max_length=300, null=True, blank=True)
    defectq = models.CharField(max_length=300, null=True, blank=True)
    unsortedq = models.CharField(max_length=300, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=3)
    stype = models.CharField(max_length=300, null=True)
    project = models.CharField(max_length=300, null=True, blank=True)
    location = models.CharField(max_length=300, null=True)
    proccessing = models.CharField(max_length=300, null=True)
    cropyear = models.CharField(max_length=300, null=True)
    varieties = models.CharField(max_length=300, null=True)
    regdate = models.CharField(max_length=300, null=True, blank=True)
    grade = models.CharField(max_length=300, null=True, blank=True)
    rating = models.CharField(max_length=300, null=True, blank=True)
    cert = models.CharField(max_length=300, null=True, blank=True)
    notes = models.TextField(max_length=300, null=True, blank=True)
    refid = models.CharField(max_length=300, null=True, blank=True)
    salenum = models.CharField(max_length=300, null=True, blank=True)
    iconum = models.CharField(max_length=300, null=True, blank=True)
    contnum = models.CharField(max_length=300, null=True, blank=True)
    tracknum = models.CharField(max_length=300, null=True, blank=True)
    country = models.CharField(max_length=300, null=True, blank=True)
    farm = models.CharField(max_length=300, null=True, blank=True)
    importer = models.CharField(max_length=300, null=True, blank=True)
    exporter = models.CharField(max_length=300, null=True, blank=True)
    wetmill = models.CharField(max_length=300, null=True, blank=True)
    drymill = models.CharField(max_length=300, null=True, blank=True)
    cooperative = models.CharField(max_length=300, null=True, blank=True)
    assosiation = models.CharField(max_length=300, null=True, blank=True)
    customer = models.CharField(max_length=300, null=True, blank=True)
    othertrac = models.TextField(max_length=300, null=True, blank=True)
    sampleweight = models.CharField(max_length=300, null=True, blank=True)
    sampleweightunit = models.CharField(max_length=300, null=True, blank=True)
    expweight = models.CharField(max_length=300, null=True, blank=True)
    expweightunit = models.CharField(max_length=300, null=True, blank=True)
    expprice = models.CharField(max_length=300, null=True, blank=True)
    exptotalprice = models.CharField(max_length=300, null=True, blank=True)
    exparrival = models.CharField(max_length=300, null=True, blank=True)
    moisture = models.CharField(max_length=300, null=True, blank=True)
    wa = models.CharField(max_length=300, null=True, blank=True)
    density = models.CharField(max_length=300, null=True, blank=True)
    physicaldefects = models.CharField(max_length=300, null=True)
    screensize = models.CharField(max_length=300, null=True, blank=True)
    classification = models.CharField(max_length=300, null=True, blank=True)
    estgreenweight = models.CharField(max_length=300, null=True, blank=True)
    sensorialdescriptors = models.TextField(max_length=300, null=True, blank=True)
    generalcomments = models.TextField(max_length=300, null=True, blank=True)
    sensorial = models.CharField(max_length=300, null=True, blank=True)
    shared_with = models.ManyToManyField(User, through='InventoryShare', related_name='shared_inventory', blank=True)
    view_perms = models.ManyToManyField(User, through='InventoryViewPerms', related_name='inventory_view_perms', blank=True)
    def __str__(self):
        return self.id
    
class InventoryShare(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    inventoryid = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    can_alter = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sample} shared with {self.user}"
    
class InventoryViewPerms(models.Model):
    #id = models.CharField(max_length=300, primary_key=True)
    inventoryid = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    sampleid = models.BooleanField(default=True)
    code = models.BooleanField(default=True)
    pricelocal = models.BooleanField(default=True)
    priceexport = models.BooleanField(default=True)
    totalq = models.BooleanField(default=True)
    g1q = models.BooleanField(default=True)
    g2q = models.BooleanField(default=True)
    g3q = models.BooleanField(default=True)
    g4q = models.BooleanField(default=True)
    g5q = models.BooleanField(default=True)
    defectq = models.BooleanField(default=True)
    unsortedq = models.BooleanField(default=True)
    name = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stype = models.BooleanField(default=False)
    project = models.BooleanField(default=False)
    location = models.BooleanField(default=True)
    proccessing = models.BooleanField(default=True)
    cropyear = models.BooleanField(default=True)
    varieties = models.BooleanField(default=True)
    regdate = models.BooleanField(default=True)
    grade = models.BooleanField(default=True)
    rating = models.BooleanField(default=False)
    cert = models.BooleanField(default=False)
    notes = models.BooleanField(default=False)
    refid = models.BooleanField(default=False)
    salenum = models.BooleanField(default=False)
    iconum = models.BooleanField(default=False)
    contnum = models.BooleanField(default=False)
    tracknum = models.BooleanField(default=False)
    country = models.BooleanField(default=True)
    farm = models.BooleanField(default=False)
    importer = models.BooleanField(default=False)
    exporter = models.BooleanField(default=False)
    wetmill = models.BooleanField(default=False)
    drymill = models.BooleanField(default=False)
    cooperative = models.BooleanField(default=False)
    assosiation = models.BooleanField(default=False)
    customer = models.BooleanField(default=False)
    othertrac = models.BooleanField(default=False)
    sampleweight = models.BooleanField(default=False)
    sampleweightunit = models.BooleanField(default=False)
    expweight = models.BooleanField(default=False)
    expweightunit = models.BooleanField(default=False)
    expprice = models.BooleanField(default=False)
    exptotalprice = models.BooleanField(default=False)
    exparrival = models.BooleanField(default=False)
    moisture = models.BooleanField(default=True)
    wa = models.BooleanField(default=True)
    density = models.BooleanField(default=True)
    physicaldefects = models.BooleanField(default=True)
    screensize = models.BooleanField(default=True)
    classification = models.BooleanField(default=False)
    estgreenweight = models.BooleanField(default=False)
    sensorialdescriptors = models.BooleanField(default=True)
    generalcomments = models.BooleanField(default=False)
    sensorial = models.BooleanField(default=True)
    can_share = models.BooleanField(default=False)
    
    def __str__(self):
        return self.id