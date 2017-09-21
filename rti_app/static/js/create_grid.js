$(function () {
// Developed this function with help from:
// http://zetcode.com/articles/jsgridservlet/
    $("#jsGrid").jsGrid({
        height: "auto",
        width: "auto",
        inserting: false,
        editing: false,
        sorting: true,
        paging: true,
        autoload: true,
        pageSize: 20,
        controller: {
            loadData: function (filter) {
                return $.ajax({
                    type: "GET",
                    url: "/show_data",
                    data: filter
                });
            },
            insertItem: $.noop,
            updateItem: $.noop,
            deleteItem: $.noop
        },
        fields: [
            { name: "Age",              type: "number", width: 40,  title:"Age"},
            { name: "Race",             type: "text",   width: 40,  title:"Race"},
            { name: "Sex",              type: "text",   width: 40,  title:"Sex"},
            { name: "Occupation",       type: "text",   width: 40,  title:"Occupation" },
            { name: "Hours Per Week",   type: "number", width: 60,  title:"Hours Per Week"},
            { name: "Work Class",       type: "text",   width: 50,  title:"Work Class"},
            { name: "Education Level",  type: "text",   width: 45,  title:"Education Level"},
            { name: "Education Num",    type: "number", width: 45,  title:"Education Num"},
            { name: "Income",           type: "number", width: 45,  title:"Income"},
            { name: "Loss",             type: "number", width: 40,  title:"Loss",},
            { name: "Over 50K",         type: "text", width: 40,  title:"Over 50K"},
            { name: "Marital Status",   type: "text",   width: 100, title:"Marital Status"},
            { name: "Relationship Name",type: "text",   width: 50,  title:"Relationship Name"},
            { name: "Country",          type: "text",   width: 50,  title:"Country"},
            { name: "Married",          type: "text", width: 30,  title:"Married?"}
        ]
    });

});