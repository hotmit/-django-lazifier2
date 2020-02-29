from django.utils.translation import ugettext_lazy as _
from crispy_forms.layout import Button, Submit
from crispy_forms.helper import FormHelper
from django_lazifier2.abstract.forms import FlowLayoutForm
from django import forms


class ActionBaseForm(forms.ModelForm, FlowLayoutForm):
    FORM_ID_PREFIX = 'frm-am-'
    FORM_CSS_CLASS = 'frm-am'

    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.helper = FormHelper()
        super().__init__(*args, **kwargs)
        self.init_dt_helper()

    def init_dt_helper(self):
        helper = getattr(self, 'helper', FormHelper())
        if self.FORM_CSS_CLASS not in helper.form_class:
            helper.form_class += ' ' + self.FORM_CSS_CLASS
        self.helper = helper


class ActionCreateForm(ActionBaseForm, forms.ModelForm):

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, request=request, **kwargs)

        helper = FormHelper()
        helper.form_method = 'POST'
        helper.form_action = 'create/'
        helper.form_id =  self.FORM_ID_PREFIX + 'create'
        helper.form_class = self.FORM_CSS_CLASS
        helper.add_input(Button('ajax-reset', _('Reset'), css_class='btn btn-warning ajax-reset'))
        helper.add_input(Submit('submit', _('Create')))

        self.helper = helper
        self.setup_flow_layout()


class ActionUpdateForm(ActionBaseForm):

    pk = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        helper = FormHelper()
        helper.form_method = 'POST'
        helper.form_action = 'update/'
        helper.form_id =  self.FORM_ID_PREFIX + 'update'
        helper.form_class = self.FORM_CSS_CLASS
        helper.add_input(Button('ajax-reset', _('Reset'), css_class='btn btn-warning ajax-reset'))
        helper.add_input(Submit('submit', _('Update')))

        if self.instance and self.instance.pk:
            self.fields['pk'].initial = self.instance.pk

        self.helper = helper
        self.setup_flow_layout()
