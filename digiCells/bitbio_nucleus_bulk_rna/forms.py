from django import forms
from django.core.exceptions import MultipleObjectsReturned
from .models import GeneCollection, Gene, AnalysisOutput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class GeneCollectionForm(forms.ModelForm):
    gene_input = forms.CharField(
        widget=forms.Textarea,
        help_text="Paste gene names or Ensembl IDs, one per line.",
    )
    linked_analysis = forms.ModelChoiceField(
        queryset=AnalysisOutput.objects.all(),
        widget=forms.HiddenInput(),
        required=False  # Mark as optional to avoid validation errors
    )

    class Meta:
        model = GeneCollection
        fields = ['collection_name', 'description', 'gene_input', 'linked_analysis']

    def __init__(self, *args, **kwargs):

        analysis = kwargs.pop('analysis_id', None)

        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save Collection'))

        # Pre-populate included_genes field
        if self.instance and self.instance.pk:
            existing_genes = []
            for a_gene in self.instance.included_genes.all():
                existing_genes.append(a_gene.ensembl_id + " - " + a_gene.gene_name)
            self.fields['gene_input'].initial = "\n".join(existing_genes)

        # Autopopulate the linked_analysis hidden field
        if analysis:
            self.fields['linked_analysis'].initial = analysis

    def clean_gene_input(self):
        gene_input = self.cleaned_data['gene_input']
        input_lines = gene_input.strip().splitlines()
        print(input_lines)
        valid_genes = []
        invalid_genes = []
        duplicated_genes = []

        for line in input_lines:
            gene_name_or_id = line.strip().split(".")[0]

            if Gene.objects.filter(gene_name=gene_name_or_id).exists():
                try:
                    valid_genes.append(Gene.objects.get(gene_name=gene_name_or_id))
                except MultipleObjectsReturned:
                    matched_genes = Gene.objects.filter(gene_name=gene_name_or_id)
                    for a_gene_obj in matched_genes:
                        duplicated_genes.append(a_gene_obj.ensembl_id + "_" + a_gene_obj.gene_name)
            elif Gene.objects.filter(ensembl_id__startswith=gene_name_or_id).exists():
                valid_genes.append(Gene.objects.get(ensembl_id__startswith=gene_name_or_id))

            else:
                invalid_genes.append(gene_name_or_id)

        if invalid_genes:
            raise forms.ValidationError(
                f"These genes could not be found: {', '.join(invalid_genes)}"
            )
        if duplicated_genes:
            raise forms.ValidationError(
                f"These genes returned multiple options, please select the correct one and provide the Ensembl ID: {', '.join(duplicated_genes)} "
            )

        # Store the valid genes in the form instance for use in the view
        self.cleaned_data['valid_genes'] = valid_genes
        return gene_input


