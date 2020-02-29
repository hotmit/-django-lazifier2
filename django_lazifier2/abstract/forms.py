from django_lazifier2.utils.django.form import Frm
from crispy_forms.helper import FormHelper
from django import forms


class FlowLayoutForm:
    strict_flow_layout = False
    flow_layout = None

    def __init__(self):
        self.helper = FormHelper()                  # type: FormHelper

    def setup_flow_layout(self):
        self.helper = getattr(self, 'helper', FormHelper())
        Frm.set_flow_layout(self, self.flow_layout, strict=self.strict_flow_layout)


class BaseForm(FlowLayoutForm):

    def add_widget_classes(self):
        fields = getattr(self, 'fields', {})

        for fn, field in fields.items():        # type: str, forms.Field
            if isinstance(field, forms.DateField):
                self.add_class(field, 'date-picker')
            elif isinstance(field, forms.ChoiceField) or isinstance(field, forms.ModelChoiceField):
                self.add_class(field, 'single-select')
            elif isinstance(field, forms.MultipleChoiceField) or isinstance(field, forms.ModelMultipleChoiceField):
                self.add_class(field, 'multiselect-select')

    @classmethod
    def add_class(cls, field: forms.Field, css_class):
        field_css_classes = field.widget.attrs.get('class', '')
        if css_class not in field_css_classes:
            field.widget.attrs['class'] = field_css_classes + ' ' + css_class


class BaseSearchForm(BaseForm):
    FORM_CSS_CLASS = 'search-form'

    def __init__(self, request):
        self.request = request
        super().__init__()

        if self.FORM_CSS_CLASS not in self.helper.form_class:
            self.helper.form_class += ' ' + self.FORM_CSS_CLASS
