import random
import django_tables2 as tables
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.templatetags.static import static


from .models import AnalysisOutput, GeneCollection, Gene


class BulkRNATable(tables.Table):
    id = tables.Column(verbose_name='Action', orderable=False)
    project = tables.Column(verbose_name='Project', orderable=False)  # Ordering is handled by JS datatable in bitbio_nucleus/static/bitbiou_nucleus/js/table_rendering.js
    product = tables.Column(verbose_name='Product', orderable=False)
    description = tables.Column(verbose_name='Description', orderable=False)
    conditions = tables.Column(verbose_name='Conditions', orderable=False)
    added_by = tables.Column(verbose_name='Added by', orderable=False)
    origin = tables.Column(verbose_name='Origin', orderable=False)
    linked_benchling_entry = tables.Column(verbose_name='Benchling entry', orderable=False)
    shiny_id = tables.Column(verbose_name='Shiny ID', orderable=False)
    created_at = tables.Column(verbose_name='Created at', orderable=False)
    updated_at = tables.Column(verbose_name='Updated at', orderable=False)
    is_visible_in_commercial_app = tables.Column(verbose_name='Commercial', orderable=False)
    metadata = tables.Column(verbose_name='metadata', orderable=False)

    def __init__(self, data, request, *args, **kwargs):
        super(BulkRNATable, self).__init__(data, *args, **kwargs)
        self.request = request

    class Meta:
        # Set column order
        fields = (
            'product', 'conditions'
        )
        exclude = (
            'id', 'project', 'added_by', 'linked_benchling_entry', 'shiny_id', 'created_at', 'updated_at',
            'is_visible_in_commercial_app', 'metadata', 'origin'
        )
        attrs = {'id': 'sortedtable'}
        template_name = "django_tables2/bootstrap.html"

        # Add `data-image` attribute to each row, setting it to the value of `image_url`
        row_attrs = {
            'data-image': lambda record: static(f"bitbio_nucleus/images/{record['product']}.png"),  # Full path to the static file
            'data-url': lambda record: reverse('bulk_rna:explore_analysis', kwargs={'analysis_id': record['id']})
        }

    def render_conditions(self, value):
        """
        Custom rendering for the 'conditions' column.
        This splits the value by commas and renders each condition in a tag-like div
        with a random background color.
        """
        if not value:
            return ''

        # List of colors to choose from
        colors = ["#FFB604", "#FF8417", "#FF512A", "#E50078"]

        # Split the conditions by commas
        conditions_list = value.split(',')

        # Wrap each condition in a div with a tag-like style and random color
        tag_html = ''.join([
            f'<div class="tag" style="background-color: {random.choice(colors)}; color: white; padding: 2px 5px; border-radius: 3px; display: inline-block; margin: 2px;">{condition.strip()}</div>'
            for condition in conditions_list
        ])

        # Return the safe HTML
        return mark_safe(tag_html)


class GeneCollectionTable(tables.Table):
    collection_name = tables.Column(verbose_name='Collection Name')
    description = tables.Column(verbose_name='Description')
    dataset = tables.Column(verbose_name='Dataset', accessor='linked_analyses')
    created_by = tables.Column(verbose_name='Created By')
    edit = tables.Column(empty_values=())   # Extra column for edit button
    delete = tables.Column(empty_values=())  # Extra column for delete button

    def __init__(self, *args, **kwargs):
        # Initialize request context to check ownership
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def render_collection_name(self, value, record):
        # Render collection name as a clickable link
        url = reverse('bulk_rna:view_gene_collection', args=[record.id])
        return format_html('<a href="{}">{}</a>', url, value)

    def render_dataset(self, record):
        """
        Render the dataset column to show the product values
        from the related AnalysisOutput objects.
        """
        # Get the product values from related AnalysisOutput objects
        products = record.linked_analyses.values_list('product', flat=True)

        # Join the product names into a single string, separated by commas
        return ", ".join(products)

    def render_edit(self, record):
        # Show edit button if the user is the owner
        if record.created_by == self.request.user:
            edit_url = reverse('bulk_rna:edit_gene_collection', args=[record.id])
            return format_html('<a href="{}" class="btn btn-warning btn-sm">Edit</a>', edit_url)
        return ''

    def render_delete(self, record):
        # Show delete button if the user is the owner
        if record.created_by == self.request.user:
            delete_url = reverse('bulk_rna:delete_gene_collection', args=[record.id])
            return format_html('<a href="{}" class="btn btn-danger btn-sm">Delete</a>', delete_url)
        return ''

    class Meta:
        model = GeneCollection
        fields = ('collection_name', 'dataset', 'description', 'created_by', 'edit', 'delete')
        attrs = {'class': 'table table-striped table-hover'}


class GeneTable(tables.Table):
    gene_name = tables.Column(verbose_name="Gene Name")
    ensembl_id = tables.Column(verbose_name="Ensembl ID")
    long_name = tables.Column(verbose_name="Long Name")

    class Meta:
        model = Gene
        fields = ('gene_name', 'ensembl_id', 'long_name')
        attrs = {'class': 'table table-striped table-hover'}


