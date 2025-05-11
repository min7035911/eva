# products/resources.py

from import_export import resources, fields
from import_export.widgets import ManyToManyWidget, CharWidget, BooleanWidget
from .models import (
    FloorMatProduct,
    InstallationOption,
    MAT_COLOR_CHOICES,
    BORDER_COLOR_CHOICES,
)

class FloorMatProductResource(resources.ModelResource):
    installation_options = fields.Field(
        column_name='Комплектация',
        attribute='installation_options',
        widget=ManyToManyWidget(InstallationOption, field='name', separator='|')
    )
    mat_color = fields.Field(
        column_name='Цвет коврика',
        attribute='mat_color',
        widget=CharWidget()   # заменили ChoiceWidget на CharWidget
    )
    border_color = fields.Field(
        column_name='Цвет окантовки',
        attribute='border_color',
        widget=CharWidget()   # заменили ChoiceWidget на CharWidget
    )
    crossbar = fields.Field(
        column_name='Перемычка',
        attribute='crossbar',
        widget=BooleanWidget()
    )
    heelpad = fields.Field(
        column_name='Подпятник',
        attribute='heelpad',
        widget=BooleanWidget()
    )

    class Meta:
        model = FloorMatProduct
        import_id_fields = ('code',)
        fields = (
            'code','name','page_title','price',
            'short_description','full_description','meta_description',
            'installation_options','mat_color','border_color',
            'crossbar','heelpad','image',
        )
        skip_unchanged = True
        report_skipped = True
        skip_errors = False
