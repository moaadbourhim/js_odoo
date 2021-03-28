odoo.define('employee_dashboard_base_test', function (require) {
    "use strict";

    console.log("Module Loaded ... ");
//    var AbstractAction = require('web.AbstractAction');
    var AbstractAction = require('web.AbstractWebClient');
    var core = require('web.core');


    var NewAction = AbstractAction.extend({
        template:'Dashboard',
        cssLibs: [
            '/employee_dashboard_base/static/src/css/style.css'
        ],
        events:{
            'click .clickMe': 'get_all_users'
        },
        init: function(){
            this._super.apply(this, arguments);
            console.log("init method")
        },
//        _render: function () {
//            var res = this._super.apply(this, arguments);
//            $("p").append(" <b>Render Template</b>.");
////            if (!this.modules) {
////                this._initModules();
////            }
////            this._renderLeftPanel();
////            this._initSearch();
////            return res;
//        },
        start: function () {
        console.log("render method")
//            this.$el.empty();

//            var $view = $(QWeb.render('ks_color_picker_opacity_view', {
//                ks_color_value: ks_color_value,
//                ks_color_opacity: ks_color_opacity
//            }));

//            this.$el.append(" <b>Render Template</b>.")
                $("p").append(" <b>Appended text</b>.");
//            this.$el.find(".ks_color_picker").spectrum({
//                color: ks_color_value,
//                showInput: true,
//                hideAfterPaletteSelect: true,
//
//                clickoutFiresChange: true,
//                showInitial: true,
//                preferredFormat: "rgb",
//            });

//            if (this.mode === 'readonly') {
//                this.$el.find('.ks_color_picker').addClass('ks_not_click');
//                this.$el.find('.ks_color_opacity').addClass('ks_not_click');
//                this.$el.find('.ks_color_picker').spectrum("disable");
//            } else {
//                this.$el.find('.ks_color_picker').spectrum("enable");
//            }
        },
        sayHello: function(){
            console.log("hello Moaad")
            $("p").append(" <b>Appended text</b>.");
        },
        get_all_users:function(){
            $("#toto").find("tr:gt(0)").remove();
            return this._rpc({model: 'person.test', method: 'get_all_persons', args: [''],})
                .then(function (result) {
                    console.log(result)
                    console.log(typeof result);
                    var i,j;
                    var add_persons = '<tr><th>Nom</th><th>Adresse</th><th>Phone</th></tr>'
                    for (i = 0; i < result.length; i++) {
                        console.log("Person : " + i)
                        add_persons = add_persons + '<tr>';
                        for(j = 0 ; j < result[i].length; j++){
                            console.log(result[i][j]);
                            add_persons = add_persons + '<td>'+result[i][j]+'</td>';
                        }
                        add_persons = add_persons + '</tr>';
                    }
                    $('#toto tr:last').after(add_persons);
                });
        }
    });

    core.action_registry.add('employee_dashboard_base_test', NewAction);
    return NewAction;
});