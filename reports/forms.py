from django import forms
from django.core.validators import RegexValidator
from django.forms import formset_factory, BaseFormSet 
from django.forms.widgets import Textarea

import datetime
# Define your choices as constants
SEX_CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Transgender', 'Transgender')]
CHC_CHOICES = [
    ('chc_barhaj', 'Community Health Centre Barhaj'),
    ('chc_bhatpar_rani', 'Community Health Centre Bhatpar Rani'),
    ('chc_gauri_bazar', 'Community Health Centre Gauri bazar'),
    ('chc_lar', 'Community Health Centre Lar'),
    ('chc_pathardeva', 'Community Health Centre Pathardeva'),
    ('chc_rudrapur', 'Community Health Centre Rudrapur'),
    ('chc_salempur', 'Community Health Centre Salempur'),
    ('chc_tarkulwa', 'Community Health Centre Tarkulwa'),
    ('chc_bhatni', 'Community Health Centre Bhatni'),
    ('chc_pipradaula_kadambri', 'Community Health Centre Pipradaula Kadambri'),
    ('phc_baitalpur', 'Primary Health Centre Baitalpur'),
    ('phc_bhaluani', 'Primary Health Centre Bhaluani'),
    ('phc_bhagalpur', 'Primary Health Centre Bhagalpur'),
    ('phc_mahen', 'Primary Health Centre Mahen'),
    ('phc_rampur_karkhana', 'Primary Health Centre Rampur Karkhana'),
    ('phc_maghgawan', 'Primary Health Centre Maghgawan'),
]

THANA_CHOICES = [
    ('baghauchghat', 'Baghauchghat'),
    ('bankata', 'Bankata'),
    ('barhaj', 'Barhaj'),
    ('bariyarpur', 'Bariyarpur'),
    ('bhaluani', 'Bhaluani'),
    ('bhatni', 'Bhatni'),
    ('bhatparrani', 'Bhatparrani'),
    ('ekauna', 'Ekauna'),
    ('gauribazar', 'Gauribazar'),
    ('khampar', 'Khampar'),
    ('khukhundu', 'Khukhundu'),
    ('kotwali_deoria', 'Kotwali Deoria'),
    ('lar', 'Lar'),
    ('madanpur', 'Madanpur'),
    ('mahuwadih', 'Mahuwadih'),
    ('mail', 'Mail'),
    ('rampur_karkhana', 'Rampur Karkhana'),
    ('rudrapur', 'Rudrapur'),
    ('salempur', 'Salempur'),
]

INJURY_TYPE = [
    ('abrasion', 'Abrasion'),
    ('laceration', 'Laceration'),
    ('abraded_laceration', 'Abraded Laceration'),
    ('sharp_cut_injury', 'Sharp cut Injury'),
    ('stab_injury', 'Stab Injury'),
    ('gunshot_injury', 'Gunshot Injury'),
    ('burn_injury', 'Burn Injury'),
    ('other', 'Other'),
]

# CHC_CHOICES = [
# 'Community Health Centre Barhaj',
# 'Community Health Centre Bhatpar Rani',
# 'Community Health Centre Gauri bazar',
# 'Community Health Centre Lar',
# 'Community Health Centre Pathardeva',
# 'Community Health Centre Rudrapur',
# 'Community Health Centre Salempur',
# 'Community Health Centre Tarkulwa',
# 'Community Health Centre Bhatni',
# 'Community Health Centre Pipradaula Kadambri',
# 'Primary Health Centre Baitalpur',
# 'Primary Health Centre Bhaluani',
# 'Primary Health Centre Bhagalpur',
# 'Primary Health Centre Mahen',
# 'Primary Health Centre Rampur Karkhana',
# 'Primary Health Centre Maghgawan'
# ]
# THANA_CHOICES = [
# 'Baghauchghat',
# 'Bankata',
# 'Barhaj',
# 'Bariyarpur',
# 'Bhaluani',
# 'Bhatni',
# 'Bhatparrani',
# 'Ekauna',
# 'Gauribazar',
# 'Khampar',
# 'Khukhundu',
# 'Kotwali Deoria',
# 'Lar',
# 'Madanpur',
# 'Mahuwadih',
# 'Mail',
# 'Rampur Karkhana',
# 'Rudrapur',
# 'Salempur'
# ]

# INJURY_TYPE = [
# 'Abrasion',
# 'Laceration',
# 'Abraded Laceration',
# 'Sharp cut Injury',
# 'Stab Injury',
# 'Gunshot Injury',
# 'Burn Injury',
# 'Other'
# ]

NATURE_CHOICES = [
    ('Simple', 'Simple'),
    ('Grievous', 'Grievous')
]

class BroughtByForm(forms.Form):
    constable_name = forms.CharField(max_length=100)
    mobile_number = forms.CharField(
        max_length=10, 
        min_length=10, 
        validators=[RegexValidator(r'^\d{10}$', message="Mobile number must be exactly 10 digits.")],
        help_text="Enter a 10-digit mobile number."
    )
    #mobile_number = forms.CharField(max_length=15, validators=[RegexValidator(r'^\d{1,15}$')])
    police_station = forms.ChoiceField(choices=THANA_CHOICES)

class GeneralConditionForm(forms.Form):
    consciousness_level = forms.CharField(max_length=100)
    pulse = forms.IntegerField(min_value=0)
    bp_systolic = forms.IntegerField(min_value=0, max_value=300, label='BP Systolic', initial=120)
    bp_diastolic = forms.IntegerField(min_value=0, max_value=200, label='BP Diastolic', initial=80)
    # bp_systolic = forms.IntegerField(min_value=0, label='BP Systolic')
    # bp_diastolic = forms.IntegerField(min_value=0, label='BP Diastolic')
    others = forms.CharField(widget=forms.Textarea, required=False)

class ReferralForm(forms.Form):
    refer_to = forms.CharField(max_length=100)
    reason_for_referral = forms.CharField(max_length=100)

class InjuryField(forms.Form):
    injury_type = forms.ChoiceField(choices=INJURY_TYPE)
    size = forms.CharField(max_length=100)
    location = forms.CharField(max_length=100)
    nature = forms.ChoiceField(choices=NATURE_CHOICES)
    caused_by = forms.CharField(max_length=100)
    duration = forms.CharField(max_length=100)
    # ... more fields ...

class BaseInjuryFormSet(BaseFormSet):
    def clean(self):
        """
        Custom validation for the formset.
        """
        if any(self.errors):
            # If any forms already have errors, don't bother validating the formset.
            return


# class BaseInjuryFormSet(BaseFormSet):
#     def clean(self):
#         """Adds validation to check that no two injuries have the same data and that all are valid."""
#         if any(self.errors):
#             return

#         injuries = []
#         duplicates = False

#         for form in self.forms:
#             if form.cleaned_data:
#                 injury = form.cleaned_data['injury_type']
#                 if injury:  # Only do something if injury is not empty.
#                     if injury in injuries:
#                         duplicates = True
#                     injuries.append(injury)

#                 if duplicates:
#                     raise forms.ValidationError('Injuries must be unique.', code='duplicate_injuries')

# Then create your formset
InjuryFormSet = formset_factory(InjuryField, formset=BaseInjuryFormSet, extra=1, can_delete=True)

class InjuryReportForm(forms.Form):
    name = forms.CharField(max_length=100)
    so_do_wo = forms.CharField(max_length=100, label="SO/DO/WO")
    address = forms.CharField(widget=forms.Textarea)
    age = forms.IntegerField(min_value=0)
    sex = forms.ChoiceField(choices=SEX_CHOICES)
    date = forms.DateField(
        initial=datetime.date.today,
        widget=forms.DateInput(attrs={'type': 'date', 'readonly': 'readonly'})
    )
    time = forms.TimeField(
        initial=datetime.datetime.now().strftime('%H:%M'),
        widget=forms.TimeInput(attrs={'type': 'time', 'readonly': 'readonly'})
    )
    # date = forms.DateField(widget=forms.HiddenInput(), initial=datetime.date.today)
    # time = forms.TimeField(widget=forms.HiddenInput(), initial=datetime.datetime.now)
    
    # date = forms.DateField(widget=forms.HiddenInput(), initial=forms.fields.DateField().today)
    # time = forms.TimeField(widget=forms.HiddenInput(), initial=forms.fields.TimeField().now)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.brought_by_form = BroughtByForm(prefix='Brought_by')
        self.general_condition_form = GeneralConditionForm(prefix='General_condition')
        self.referral_form = ReferralForm(prefix='Referral')
        self.injuries = InjuryField(prefix='Injuries')
    # constable_name = forms.CharField(max_length=100)
    # mobile_number = forms.CharField(max_length=15)
    # police_station = forms.ChoiceField(choices=THANA_CHOICES)
    # Nested forms
    # brought_by = BroughtByForm(prefix='brought_by')
    # general_condition = GeneralConditionForm(prefix='general_condition')
    # referral = ReferralForm(prefix='referral')
    # ... more fields ...
    
# class SexualViolenceReportForm(BaseReportForm):
#     # Specific fields for this report type
#     assault_date = forms.DateField()
#     consent = forms.BooleanField(required=False)
    # More specific fields...
