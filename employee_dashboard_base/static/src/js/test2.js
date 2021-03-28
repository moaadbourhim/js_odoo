odoo.define('employee_dashboard_base_test2', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractWebClient');
    var core = require('web.core');


    var NewAction = AbstractAction.extend({

        init: function(){
            this._super.apply(this, arguments);
            console.log("Test 2")
        },

    });

    core.action_registry.add('employee_dashboard_base_test2', NewAction);
    return NewAction;
});