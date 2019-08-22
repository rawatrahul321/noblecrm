noblecrm.define('iap.redirect_noblecrm_credit_widget', function(require) {
"use strict";

var core = require('web.core');
var framework = require('web.framework');
var Widget = require('web.Widget');
var QWeb = core.qweb;


var IapNobleCRMCreditRedirect = Widget.extend({
    template: 'iap.redirect_to_noblecrm_credit',
    events : {
        "click .redirect_confirm" : "noblecrm_redirect",
    },
    init: function (parent, action) {
        this._super(parent, action);
        this.url = action.params.url;
    },

    noblecrm_redirect: function () {
        window.open(this.url, '_blank');
        this.do_action({type: 'ir.actions.act_window_close'});
        // framework.redirect(this.url);
    },

});
core.action_registry.add('iap_noblecrm_credit_redirect', IapNobleCRMCreditRedirect);
});
