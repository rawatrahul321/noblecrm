noblecrm.define('web.KanbanView', function (require) {
"use strict";

var BasicView = require('web.BasicView');
var core = require('web.core');
var config = require('web.config');
var KanbanModel = require('web.KanbanModel');
var KanbanRenderer = require('web.KanbanRenderer');
var KanbanController = require('web.KanbanController');
var utils = require('web.utils');

var _lt = core._lt;

var KanbanView = BasicView.extend({
    accesskey: "k",
    display_name: _lt("Kanban"),
    icon: 'fa-th-large',
    mobile_friendly: true,
    config: {
        Model: KanbanModel,
        Controller: KanbanController,
        Renderer: KanbanRenderer,
    },
    jsLibs: [],
    viewType: 'kanban',

    /**
     * @constructor
     */
    init: function (viewInfo, params) {
        this._super.apply(this, arguments);

        var arch = viewInfo.arch;

        this.loadParams.limit = this.loadParams.limit || 40;
        // in mobile, columns are lazy-loaded, so set 'openGroupByDefault' to
        // false so that they will won't be loaded by the initial load
        this.loadParams.openGroupByDefault = config.device.isMobile ? false : true;
        this.loadParams.type = 'list';
        this.loadParams.groupBy = arch.attrs.default_group_by ? [arch.attrs.default_group_by] : (params.groupBy || []);
        var progressBar;
        utils.traverse(arch, function (n) {
            var isProgressBar = (n.tag === 'progressbar');
            if (isProgressBar) {
                progressBar = _.clone(n.attrs);
                progressBar.colors = JSON.parse(progressBar.colors);
                progressBar.sum_field = progressBar.sum_field || false;
            }
            return !isProgressBar;
        });
        if (progressBar) {
            this.loadParams.progressBar = progressBar;
        }

        var activeActions = this.controllerParams.activeActions;
        activeActions = _.extend(activeActions, {
            group_create: arch.attrs.group_create ? JSON.parse(arch.attrs.group_create) : true,
            group_edit: arch.attrs.group_edit ? JSON.parse(arch.attrs.group_edit) : true,
            group_delete: arch.attrs.group_delete ? JSON.parse(arch.attrs.group_delete) : true,
        });

        this.rendererParams.column_options = {
            editable: activeActions.group_edit,
            deletable: activeActions.group_delete,
            group_creatable: activeActions.group_create && !config.device.isMobile,
            hasProgressBar: !!progressBar,
        };
        this.rendererParams.record_options = {
            editable: activeActions.edit,
            deletable: activeActions.delete,
            read_only_mode: params.readOnlyMode,
        };
        this.rendererParams.quickCreateEnabled = this._isQuickCreateEnabled(viewInfo);

        this.controllerParams.on_create = arch.attrs.on_create;
        this.controllerParams.readOnlyMode = false;
        this.controllerParams.hasButtons = true;
        this.controllerParams.quickCreateEnabled = this.rendererParams.quickCreateEnabled;

        if (config.device.isMobile) {
            this.jsLibs.push('/web/static/lib/jquery.touchSwipe/jquery.touchSwipe.js');
        }
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * @private
     * @param {Object} viewInfo
     * @returns {boolean} true iff the quick create feature is not explicitely
     *   disabled (with create="False" or quick_create="False" in the arch)
     */
    _isQuickCreateEnabled: function (viewInfo) {
        if (!this.controllerParams.activeActions.create) {
            return false;
        }
        if (viewInfo.arch.attrs.quick_create !== undefined) {
            return JSON.parse(viewInfo.arch.attrs.quick_create);
        }
        return true;
    },
});

return KanbanView;

});
