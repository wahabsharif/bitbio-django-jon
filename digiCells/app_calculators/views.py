from django.shortcuts import render
from .forms import SeedingCalculatorForm
from .utils import compute_seeding_result



def calculators_list(request):
    return render(request, 'calculators/calculators_list.html', {})


def cell_seeding_calculator_view(request):
    result = None
    if request.method == 'POST':
        form = SeedingCalculatorForm(request.POST)
        if form.is_valid():
            result = compute_seeding_result(form.cleaned_data)
    else:
        form = SeedingCalculatorForm()

    return render(request, 'cell_seeding_calculator.html', {
        'form': form,
        'result': result
    })

