# reports/views.py

from django.forms import formset_factory
from django.shortcuts import render
from .forms import BaseInjuryFormSet, InjuryReportForm, BroughtByForm, GeneralConditionForm, ReferralForm, InjuryField, InjuryFormSet

from django.http import HttpResponse
from django.template.loader import render_to_string
#from weasyprint import HTML
from xhtml2pdf import pisa

def home(request):
    # This will be the view for your home page with buttons
    #print("Home view is being called")
    return render(request, 'home.html')

# views.py

def injury_report(request):
    InjuryFormSet = formset_factory(InjuryField, formset=BaseInjuryFormSet, extra=1, can_delete=True)

    form = InjuryReportForm()
    brought_by_form = BroughtByForm(prefix='Brought_by')
    general_condition_form = GeneralConditionForm(prefix='General_condition')
    referral_form = ReferralForm(prefix='Referral')
    #injuries_forms = [InjuryField(prefix='injury_0')]
    injury_formset = InjuryFormSet(prefix='injuries')

    if request.method == 'POST':
        form = InjuryReportForm(request.POST)
        brought_by_form = BroughtByForm(request.POST, prefix='Brought_by')
        general_condition_form = GeneralConditionForm(request.POST, prefix='General_condition')
        referral_form = ReferralForm(request.POST, prefix='Referral')
        injury_formset = InjuryFormSet(request.POST, prefix='injuries')
        # Initialize with one injury form
        # Handling multiple injury forms
        # injury_forms = []
        # injury_data = []
        # injury_count = int(request.POST.get('injury_count', 1))

        # for i in range(injury_count):
        #     injury_form = InjuryField(request.POST, prefix=f'injury_{i}')
        #     injury_forms.append(injury_form)
        #     if injury_form.is_valid():
        #         injury_data.append(injury_form.cleaned_data)

        # Check if all forms are valid
        # if (form.is_valid() and brought_by_form.is_valid() and
        #         general_condition_form.is_valid() and referral_form.is_valid() and
        #         #all(injury_form.is_valid() for injury_form in injury_forms)):
        #         injury_formset.is_valid()):
        if all([form.is_valid(), brought_by_form.is_valid(), general_condition_form.is_valid(), referral_form.is_valid(), injury_formset.is_valid()]):

            report_data = {
                'form_data': {k: (v.isoformat() if hasattr(v, 'isoformat') else v) for k, v in form.cleaned_data.items()},
                'brought_by_data': brought_by_form.cleaned_data,
                'general_condition_data': general_condition_form.cleaned_data,
                'referral_data': referral_form.cleaned_data,
                'injuries_data': [form.cleaned_data for form in injury_formset]
                #'injuries_data': injury_data  # Now using injury_data instead of injuries_form.cleaned_data
            }
            request.session['report_data'] = report_data
            return render(request, 'display_injury_report.html', {'report_data': report_data})
        else:
            #print(form.errors)
            # Here you need to add the code that handles the errors
            # For now, I'm just printing them to the console
            # Log form data for debugging
            print("POST data:", request.POST)
            print("Form errors:", form.errors)
            print("Brought by form errors:", brought_by_form.errors)
            print("General condition form errors:", general_condition_form.errors)
            print("Referral form errors:", referral_form.errors)
            print("Injury formset errors:", injury_formset.errors)
            print("Injury formset non-form errors:", injury_formset.non_form_errors())
            # for injury_form in injury_forms:
            #     print("Injury form errors:", injury_form.errors)
    # else:
    #     injuries_forms = [InjuryField(prefix='injury_0')]
    
    context = {
        'form': form,
        'brought_by_form': brought_by_form,
        'general_condition_form': general_condition_form,
        'referral_form': referral_form,
        'injury_formset': injury_formset
       # 'injuries_forms': injuries_forms  # This will now pass a list of forms
    }
    return render(request, 'injury_report_form.html', context)

def download_pdf(request):
    # Fetch or reconstruct the data for the report
    report_data = request.session.get('report_data')
    
    if report_data is None:
        # Handle the case where report_data is not found
        return HttpResponse("Error: Report data not found.", status=404)

    # Render the HTML template with report data
    html_string = render_to_string('display_injury_report.html', {
        'report_data': report_data,
        'pdf': True # Add a flag to indicate PDF generation
        })

    # Convert HTML to PDF
    # html = HTML(string=html_string)
    # pdf = html.write_pdf()

    # Create HTTP response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    # Generate PDF
    pisa_status = pisa.CreatePDF(html_string, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
    
    return response