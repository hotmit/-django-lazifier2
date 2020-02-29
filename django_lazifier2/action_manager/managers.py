from django_lazifier2.utils.django.ajax import Ajx
from django.utils.translation import ugettext as _
from django.shortcuts import render
from django.urls import reverse


class ActionManager:

    def __init__(self, request, model):
        self.request = request
        self.model = model
        self.errors = []
        self.form = None
        self.success_message = None

        self.form_template = 'action_manager/action_ajax_form.html'
        self.reset_form = request.POST.get('submit-via', '') == 'ajax-reset'
        self.has_data = bool(request.POST)

        self.context = {
            'action_manager': {
                'errors': self.errors,
                'form': self.form,
            }
        }

    def can_process(self):
        return self.has_data

    def get_context(self, *kwargs):
        self.context['action_manager'].update(kwargs)
        self.context['action_manager']['errors'] = self.errors
        self.context['action_manager']['form'] = self.form
        return self.context

    def success_action_event(self, message=None):
        return Ajx.send_ajax_command(message or self.success_message, Ajx.DisplayMethod.toastr,
                                     js_on_post_parse='refreshDataTable')

    def refresh_page_event(self, message=None):
        return Ajx.send_ajax_command(message or self.success_message, Ajx.DisplayMethod.toastr,
                                     command=Ajx.Command.refresh)

    def return_form_template(self):
        return render(self.request, self.form_template, self.get_context())

    @classmethod
    def get_api_url(cls, basename, keep=None):
        """
        Get the api url for the datatable

        :param basename: the basename used when register drf router (if not specified then the model name would be use)
        :param keep: column to always keep
        :return: url
        """
        api_url = reverse('{}-list'.format(basename))
        api_url = '{}?format=datatables'.format(api_url)
        if keep:
            return '{}&keep={}'.format(api_url, ','.join(keep))
        return api_url


class CreateManager(ActionManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class InstanceManager(ActionManager):

    def __init__(self, request, model):
        specified_pk = request.POST.get('pk', request.GET.get('pk', False))
        self.instance = model.objects.filter(pk=specified_pk).first()

        super().__init__(request, model)

        if not self.instance_found():
            self.errors = [
                _('The record you selected does not exist.')
            ]

    def instance_found(self):
        return bool(self.instance)

    def can_process(self):
        return self.has_data and self.instance_found()


class UpdateManager(InstanceManager):

    def __init__(self, request, model):
        super().__init__(request, model)
        self.success_message = _('The selected record has been updated successfully.')


class DeleteManager(InstanceManager):

    def __init__(self, request, model):
        super().__init__(request, model)
        self.success_message = _('The selected record has been deleted successfully.')

    def not_found_message(self):
        return Ajx.send_ajax_command(_('The selected record does not exist.'),
                                     display_method=Ajx.DisplayMethod.bs_dialog,
                                     status=Ajx.Status.error)


class ActionManager(InstanceManager):

    def __init__(self, request, model):
        super().__init__(request, model)
        self.action = request.POST.get('action', None)
        self.success_message = _('The action has been perform successfully.')

    def not_found_message(self):
        return Ajx.send_ajax_command(_('The selected record does not exist.'),
                                     display_method=Ajx.DisplayMethod.bs_dialog,
                                     status=Ajx.Status.error)

    def invalid_action_message(self):
        return Ajx.send_ajax_command(_('The specified action is not valid.'),
                                     display_method=Ajx.DisplayMethod.bs_dialog,
                                     status=Ajx.Status.error)
