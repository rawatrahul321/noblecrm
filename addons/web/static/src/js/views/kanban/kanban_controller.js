noblecrm.define('web.KanbanController', function (require) {
"use strict";

/**
 * The KanbanController is the class that coordinates the kanban model and the
 * kanban renderer.  It also makes sure that update from the search view are
 * properly interpreted.
 */

var BasicController = require('web.BasicController');
var Context = require('web.Context');
var core = require('web.core');
var Domain = require('web.Domain');
var view_dialogs = require('web.view_dialogs');
var viewUtils = require('web.viewUtils');

var _t = core._t;
var qweb = core.qweb;

var KanbanController = BasicController.extend({
    custom_events: _.extend({}, BasicController.prototype.custom_events, {
        quick_create_add_column: '_onAddColumn',
        quick_create_record: '_onQuickCreateRecord',
        resequence_columns: '_onResequenceColumn',
        button_clicked: '_onButtonClicked',
        kanban_record_delete: '_onRecordDelete',
        kanban_record_update: '_onUpdateRecord',
        kanban_column_delete: '_onDeleteColumn',
        kanban_column_add_record: '_onAddRecordToColumn',
        kanban_column_resequence: '_onColumnResequence',
        kanban_column_archive_records: '_onArchiveRecords',
        kanban_load_more: '_onLoadMore',
        kanban_load_records: '_onLoadColumnRecords',
        column_toggle_fold: '_onToggleColumn',
    }),
    /**
     * @override
     * @param {Object} params
     * @param {boolean} params.quickCreateEnabled set to false to disable the
     *   quick create feature
     */
    init: function (parent, model, renderer, params) {
        this._super.apply(this, arguments);

        this.on_create = params.on_create;
        this.hasButtons = params.hasButtons;

        this.createColumnEnabled = this._isCreateColumnEnabled();
        this.quickCreateEnabled = params.quickCreateEnabled;
    },

    //--------------------------------------------------------------------------
    // Public
    //--------------------------------------------------------------------------

    /**
     * @param {jQueryElement} $node
     */
    renderButtons: function ($node) {
        if (this.hasButtons && this.is_action_enabled('create')) {
            this.$buttons = $(qweb.render('KanbanView.buttons', {widget: this}));
            this.$buttons.on('click', 'button.o-kanban-button-new', this._onButtonNew.bind(this));
            this._updateButtons();
            this.$buttons.appendTo($node);
        }
    },
    /**
     * Override update method to recompute createColumnEnabled.
     *
     * @returns {Deferred}
     */
    update: function () {
        this.createColumnEnabled = this._isCreateColumnEnabled();
        return this._super.apply(this, arguments);
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * @override method comes from field manager mixin
     * @private
     * @param {string} id local id from the basic record data
     * @returns {Deferred}
     */
    _confirmSave: function (id) {
        var data = this.model.get(this.handle, {raw: true});
        var grouped = data.groupedBy.length;
        if (grouped) {
            var columnState = this.model.getColumn(id);
            return this.renderer.updateColumn(columnState.id, columnState);
        }
        return this.renderer.updateRecord(this.model.get(id));
    },
    /**
     * The column quick create should be displayed in kanban iff grouped by an
     * m2o field and group_create action enabled.
     *
     * @private
     * @returns {boolean}
     */
    _isCreateColumnEnabled: function () {
        var groupCreate = this.is_action_enabled('group_create');
        if (!groupCreate) {
            // pre-return to avoid a lot of the following processing
            return false;
        }
        var state = this.model.get(this.handle, {raw: true});
        var groupByField = state.fields[state.groupedBy[0]];
        var groupedByM2o = groupByField && (groupByField.type === 'many2one');
        return groupedByM2o;
    },
    /**
     * @param {number[]} ids
     * @private
     * @returns {Deferred}
     */
    _resequenceColumns: function (ids) {
        var state = this.model.get(this.handle, {raw: true});
        var model = state.fields[state.groupedBy[0]].relation;
        return this.model.resequence(model, ids, this.handle);
    },
    /**
     * This method calls the server to ask for a resequence.  Note that this
     * does not rerender the user interface, because in most case, the
     * resequencing operation has already been displayed by the renderer.
     *
     * @private
     * @param {string} column_id
     * @param {string[]} ids
     * @returns {Deferred}
     */
    _resequenceRecords: function (column_id, ids) {
        var self = this;
        return this.model.resequence(this.modelName, ids, column_id).then(function () {
            self._updateEnv();
        });
    },
    /**
     * In grouped mode, set 'Create' button as btn-default if there is no column
     * (except if we can't create new columns)
     *
     * @private
     * @override from abstract controller
     */
    _updateButtons: function () {
        if (this.$buttons) {
            var data = this.model.get(this.handle, {raw: true});
            var grouped = data.groupedBy.length;
            var createMuted = grouped && data.data.length === 0 && this.createColumnEnabled;
            this.$buttons.find('.o-kanban-button-new')
                .toggleClass('btn-primary', !createMuted)
                .toggleClass('btn-default', createMuted);
        }
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * This handler is called when an event (from the quick create add column)
     * event bubbles up. When that happens, we need to ask the model to create
     * a group and to update the renderer
     *
     * @private
     * @param {NobleCRMEvent} event
     */
    _onAddColumn: function (event) {
        var self = this;
        this.model.createGroup(event.data.value, this.handle).then(function () {
            var state = self.model.get(self.handle, {raw: true});
            var ids = _.pluck(state.data, 'res_id').filter(_.isNumber);
            return self._resequenceColumns(ids);
        }).then(function () {
            return self.update({}, {reload: false});
        }).then(function () {
            self._updateButtons();
            self.renderer.quickCreateToggleFold();
        });
    },
    /**
     * @private
     * @param {NobleCRMEvent} event
     */
    _onAddRecordToColumn: function (event) {
        var self = this;
        var record = event.data.record;
        var column = event.target;
        this.alive(this.model.moveRecord(record.db_id, column.db_id, this.handle))
            .then(function (column_db_ids) {
                return self._resequenceRecords(column.db_id, event.data.ids)
                    .then(function () {
                        _.each(column_db_ids, function (db_id) {
                            var data = self.model.get(db_id);
                            self.renderer.updateColumn(db_id, data);
                        });
                    });
            }).fail(this.reload.bind(this));
    },
    /**
     * The interface allows in some case the user to archive a column. This is
     * what this handler is for.
     *
     * @private
     * @param {NobleCRMEvent} event
     */
    _onArchiveRecords: function (event) {
        var self = this;
        var active_value = !event.data.archive;
        var column = event.target;
        var record_ids = _.pluck(column.records, 'db_id');
        if (record_ids.length) {
            this.model
                .toggleActive(record_ids, active_value, column.db_id)
                .then(function (db_id) {
                    var data = self.model.get(db_id);
                    self.renderer.updateColumn(db_id, data);
                    self._updateEnv();
                });
        }
    },
    /**
     * @private
     * @param {NobleCRMEvent} event
     */
    _onButtonClicked: function (event) {
        event.stopPropagation();
        var self = this;
        var attrs = event.data.attrs;
        var record = event.data.record;
        if (attrs.context) {
            attrs.context = new Context(attrs.context)
                .set_eval_context({
                    active_id: record.res_id,
                    active_ids: [record.res_id],
                    active_model: record.model,
                });
        }
        this.trigger_up('execute_action', {
            action_data: attrs,
            env: {
                context: record.getContext(),
                currentID: record.res_id,
                model: record.model,
                resIDs: record.res_ids,
            },
            on_closed: function () {
                var recordModel = self.model.localData[record.id];
                var group = self.model.localData[recordModel.parentID];
                var parent = self.model.localData[group.parentID];

                self.model.reload(record.id).then(function (db_id) {
                    var data = self.model.get(db_id);
                    var kanban_record = event.target;
                    kanban_record.update(data);

                    // Check if we still need to display the record. Some fields of the domain are
                    // not guaranteed to be in data. This is for example the case if the action
                    // contains a domain on a field which is not in the Kanban view. Therefore,
                    // we need to handle multiple cases based on 3 variables:
                    // domInData: all domain fields are in the data
                    // activeInDomain: 'active' is already in the domain
                    // activeInData: 'active' is available in the data
                    
                    var domain = (parent ? parent.domain : group.domain) || [];
                    var domInData = _.every(domain, function (d) {
                        return d[0] in data.data;
                    });
                    var activeInDomain = _.pluck(domain, 0).indexOf('active') !== -1;
                    var activeInData = 'active' in data.data;

                    // Case # | domInData | activeInDomain | activeInData
                    //   1    |   true    |      true      |      true     => no domain change
                    //   2    |   true    |      true      |      false    => not possible
                    //   3    |   true    |      false     |      true     => add active in domain
                    //   4    |   true    |      false     |      false    => no domain change
                    //   5    |   false   |      true      |      true     => no evaluation
                    //   6    |   false   |      true      |      false    => no evaluation
                    //   7    |   false   |      false     |      true     => replace domain
                    //   8    |   false   |      false     |      false    => no evaluation

                    // There are 3 cases which cannot be evaluated since we don't have all the
                    // necessary information. The complete solution would be to perform a RPC in
                    // these cases, but this is out of scope. A simpler one is to do a try / catch.

                    if (domInData && !activeInDomain && activeInData) {
                        domain = domain.concat([['active', '=', true]]);
                    } else if (!domInData && !activeInDomain && activeInData) {
                        domain = [['active', '=', true]];
                    }
                    try {
                        var visible = new Domain(domain).compute(data.evalContext);
                    } catch (e) {
                        return;
                    }
                    if (!visible) {
                        kanban_record.destroy();
                    }
                });
            },
        });
    },
    /**
     * @private
     */
    _onButtonNew: function () {
        var state = this.model.get(this.handle, {raw: true});
        var quickCreateEnabled = this.quickCreateEnabled && viewUtils.isQuickCreateEnabled(state);
        if (this.on_create === 'quick_create' && quickCreateEnabled && state.data.length) {
            // Activate the quick create in the first column
            this.renderer.addQuickCreate();
        } else if (this.on_create && this.on_create !== 'quick_create') {
            // Execute the given action
            this.do_action(this.on_create, {
                on_close: this.reload.bind(this),
                additional_context: state.context,
            });
        } else {
            // Open the form view
            this.trigger_up('switch_view', {
                view_type: 'form',
                res_id: undefined
            });
        }
    },
    /**
     * @private
     * @param {NobleCRMEvent} event
     */
    _onColumnResequence: function (event) {
        this._resequenceRecords(event.target.db_id, event.data.ids);
    },
    /**
     * @private
     * @param {NobleCRMEvent} event
     */
    _onDeleteColumn: function (event) {
        var self = this;
        var column = event.target;
        var state = this.model.get(this.handle, {raw: true});
        var relatedModelName = state.fields[state.groupedBy[0]].relation;
        this.model
            .deleteRecords([column.db_id], relatedModelName)
            .done(function () {
                if (column.isEmpty()) {
                    self.renderer.removeWidget(column);
                    self._updateButtons();
                } else {
                    self.reload();
                }
            });
    },
    /**
     * Loads the record of a given column (used in mobile, as the columns are
     * lazy loaded)
     *
     * @private
     * @param {NobleCRMEvent} event
     */
    _onLoadColumnRecords: function (event) {
        var self = this;
        this.model.loadColumnRecords(event.data.columnID).then(function (dbID) {
            var data = self.model.get(dbID);
            self.renderer.updateColumn(dbID, data);
            self._updateEnv();
            if (event.data.onSuccess) {
                event.data.onSuccess();
            }
        });
    },
    /**
     * @private
     * @param {NobleCRMEvent} event
     */
    _onLoadMore: function (event) {
        var self = this;
        var column = event.target;
        this.model.loadMore(column.db_id).then(function (db_id) {
            var data = self.model.get(db_id);
            self.renderer.updateColumn(db_id, data);
            self._updateEnv();
        });
    },
    /**
     * @private
     * @param {NobleCRMEvent} event
     */
    _onQuickCreateRecord: function (event) {
        var self = this;
        var column = event.target;
        var name = event.data.value;
        var state = this.model.get(this.handle, {raw: true});
        var columnState = this.model.get(column.db_id, {raw: true});
        var context = columnState.getContext();
        context['default_' + state.groupedBy[0]] = columnState.res_id;

        this._rpc({
                model: state.model,
                method: 'name_create',
                args: [name],
                context: context,
            })
            .then(add_record)
            .fail(function (error, event) {
                event.preventDefault();
                new view_dialogs.FormViewDialog(self, {
                    res_model: state.model,
                    context: _.extend({default_name: name}, context),
                    title: _t("Create"),
                    disable_multiple_selection: true,
                    on_saved: function (record) {
                        add_record([record.res_id]);
                    },
                }).open();
            });

        function add_record(records) {
            return self.model
                .addRecordToGroup(columnState.id, records[0])
                .then(function (db_id) {
                    self._updateEnv();

                    var columnState = self.model.getColumn(db_id);
                    return self.renderer
                        .updateColumn(columnState.id, columnState, {openQuickCreate: true})
                        .then(function () {
                            if (event.data.openRecord) {
                                self.trigger_up('open_record', {id: db_id, mode: 'edit'});
                            }
                        });
                });
        }
    },
    /**
     * @private
     * @param {NobleCRMEvent} event
     */
    _onRecordDelete: function (event) {
        this._deleteRecords([event.data.id]);
    },
    /**
     * @private
     * @param {NobleCRMEvent} event
     */
    _onResequenceColumn: function (event) {
        var self = this;
        this._resequenceColumns(event.data.ids).then(function () {
            self._updateEnv();
        });
    },
    /**
     * @private
     * @param {NobleCRMEvent} event
     * @param {boolean} [event.data.openQuickCreate=false] if true, opens the
     *   QuickCreate in the toggled column (it assumes that we are opening it)
     */
    _onToggleColumn: function (event) {
        var self = this;
        var column = event.target;
        this.model.toggleGroup(column.db_id).then(function (db_id) {
            var data = self.model.get(db_id);
            var options = {
                openQuickCreate: !!event.data.openQuickCreate,
            };
            self.renderer.updateColumn(db_id, data, options);
            self._updateEnv();
        });
    },
    /**
     * @todo should simply use field_changed event...
     *
     * @private
     * @param {NobleCRMEvent} ev
     */
    _onUpdateRecord: function (ev) {
        var changes = _.clone(ev.data);
        ev.data.force_save = true;
        this._applyChanges(ev.target.db_id, changes, ev);
    },
});

return KanbanController;

});
