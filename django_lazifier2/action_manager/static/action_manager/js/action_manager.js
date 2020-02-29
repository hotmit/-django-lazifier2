/*global jQuery, URI, Str, gettext, UI, ActionManager */

(function (global, $) {
    "use strict";

    global.ActionManager = {
        initialize: function(){

        },
        refreshDataTable: function (options, ajaxCommand) {
            $('table.datatable').DataTable().ajax.reload();
        },
    };

    $(function () {
        var $body = $('body'), $dtTable = $('table.datatable'), dialogOptions, uriSearch;

        /**
         * Get the bs dialog options from the data attrs from the source element.
         *
         * @param $src - the html element
         * @rtype: {object}
         */
        function getDialogOption($src){
            var opts = {};
            $.each($src.data(), function(key, value){
                if (Str.startsWith(key, 'bsDialog')){
                    opts[Str.toCamelCase(key.replace('bsDialog', ''))] = value;
                }
            });
            return opts;
        }

        dialogOptions = $.extend({}, {
            closeByBackdrop: false
        }, getDialogOption($dtTable));

        uriSearch = new URI().search(true);

        $body.on('click', '.btn-am-create', function(){
            var $this = $(this), data = $.extend({}, uriSearch, $this.data()), ajaxOptions = {
                url: 'create/',
                method: 'GET',
                data: data,
                dataType: 'html',
                traditional: true
            }, $dialog = UI.Patterns.bsDialogAjax(gettext('Create New'), ajaxOptions, dialogOptions, function(){
                UI.Patterns.submitForm('.frm-am', '.ajax-form-container', null, null, $dialog, null, ActionManager);
            });
        });  // End am-create

        $body.on('click', '.btn-am-edit', function(){
            var $this = $(this), data = $.extend({}, uriSearch, $this.data(), { pk: $this.parents('tr').attr('id') }), ajaxOptions = {
                url: 'update/',
                method: 'GET',
                data: data,
                dataType: 'html',
                traditional: true
            }, $dialog = UI.Patterns.bsDialogAjax(gettext('Update'), ajaxOptions, dialogOptions, function(){
                UI.Patterns.submitForm('.frm-am', '.ajax-form-container', null, null, $dialog, null, ActionManager);
            });
        }); // End am-edit

        $body.on('click', '.btn-am-delete', function(){
            var $this = $(this), data = $.extend({}, uriSearch, $this.data(), {
                    pk: $this.parents('tr').attr('id'),
                    csrfmiddlewaretoken: $.cookie('csrftoken')
                });

            UI.Bs.confirmYesNo(gettext('Are you sure you want to delete this record?'),
                function(result){
                    if (result === true){
                        var ajaxOptions = {
                            url: 'delete/',
                            method: 'POST',
                            data: data,
                            dataType: 'html',
                            traditional: true
                        };

                        UI.Patterns.submitAjaxRequest(ajaxOptions, null, null, ActionManager);
                    }
                }
            );
        });  // End am-delete

        $body.on('click', '.btn-am-action', function(){
            var $this = $(this),
                data = $.extend({}, uriSearch, $this.data(), {
                    pk: $this.parents('tr').attr('id'),
                    csrfmiddlewaretoken: $.cookie('csrftoken')
                }),
                ajaxOptions = {
                    url: $this.data('url') || 'manage/',
                    method: 'POST',
                    data: data,
                    dataType: 'html',
                    traditional: true
                };

            function _submitRequest(){
                UI.Patterns.submitAjaxRequest(ajaxOptions, '.datatable');
            }

            if (data.hasOwnProperty('confirm')){
                var confirmMsg = data.hasOwnProperty('confirmMsg') ? data.confirmMsg :
                    gettext('Are you sure you want to continue?');

                delete data.confirm;
                delete data.confirmMsg;

                UI.Bs.confirmYesNo(confirmMsg,
                    function(result){
                        if (result === true){
                            _submitRequest();
                        }
                    }
                );
            }
            else {
                _submitRequest();
            }
        });  // End am-action

        $body.on('click', '.dt-action-btn.dt-modal-dialog', function(){
            var $this = $(this),
                data = $.extend({}, uriSearch, $this.data(), { mode: 'custom' }),
                btnDialogOption = getDialogOption($this) || dialogOptions,
                ajaxOptions = {
                    url: $this.data('url') || 'manage/',
                    method: 'GET',
                    data: data,
                    dataType: 'html',
                    traditional: true
                }, $dialog = UI.Patterns.bsDialogAjax(btnDialogOption.title || '', ajaxOptions, btnDialogOption,
                function(){
                    UI.Patterns.submitForm('form.dt-ajax-form', '.dt-ajax-container',
                        null, null, $dialog);
                });
        }); // End am-dialog
    }); // End DOM Ready
}(window, jQuery));
