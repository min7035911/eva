# products/admin.py

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import InstallationOption, FloorMatProduct
from .resources import FloorMatProductResource

@admin.register(InstallationOption)
class InstallationOptionAdmin(admin.ModelAdmin):
    list_display = ("name", "extra_price")

@admin.register(FloorMatProduct)
class FloorMatProductAdmin(ImportExportModelAdmin):
    resource_class = FloorMatProductResource

    list_display = (
        "code",
        "name",
        "price",
        "mat_color",
        "border_color",
        "crossbar",
        "heelpad",
        "created",
    )
    list_filter = (
        "mat_color",
        "border_color",
        "crossbar",
        "heelpad",
        "installation_options",
    )
    search_fields = ("code", "name")
    filter_horizontal = ("installation_options",)
