from django.contrib import admin
from .models import (Region, Country, Section, Subsection, Indicator,
    IndicatorScore)


class IndicatorScoreInline(admin.TabularInline):
    model = IndicatorScore


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    pass


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", "region")
    prepopulated_fields = {"slug": ["name"]}


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    pass


@admin.register(Subsection)
class SubsectionAdmin(admin.ModelAdmin):
    pass


@admin.register(Indicator)
class IndicatorAdmin(admin.ModelAdmin):
    inlines = [IndicatorScoreInline]
    list_display = ("number", "name", "subsection")
    list_display_links = ("number", "name")
