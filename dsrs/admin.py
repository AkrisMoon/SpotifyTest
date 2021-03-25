from django.contrib import admin
from dsrs import models
# Register your models here.
@admin.decorators.register(models.DSR)
class DSRAdmin(admin.ModelAdmin):
    pass

@admin.decorators.register(models.Territory)
class TerritoryAdmin(admin.ModelAdmin):
    pass

@admin.decorators.register(models.Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass

@admin.decorators.register(models.Artist)
class ArtistAdmin(admin.ModelAdmin):
    pass

@admin.decorators.register(models.Statistics)
class StatisticsAdmin(admin.ModelAdmin):
    pass

@admin.decorators.register(models.Recording)
class RecordingAdmin(admin.ModelAdmin):
    pass