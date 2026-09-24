// Copyright (c) 2026, Suba and contributors
// For license information, please see license.txt

frappe.ui.form.on("Stay Card", {
	// setup(frm) {
    //     if(frm.doc.purpose == "Boarding")
    //         frm.set_query("assigned_attendant",() => {
    //             return{
    //                 filters:{
    //                     status: "Active",
    //                 }
    //             }
    //         })
	//     },


    refresh(frm){
        if(frm.doc.status=="Ready for Pickup"){
            frm.dashboard.add_indicator ("Ready for Pickup","Orange");
        }
        else if(frm.doc.status=="Picked Up"){
            frm.dashboard.add_indicator("Picked Up","Green")
        }
        else{
            frm.dashboard.add_indicator(frm.doc.status,"Blue")
        }    
        
        if(frm.doc.status =="Ready for Pickup" && frm.doc.docstatus==1){
            frm.add_custom_button("Mark as Picked up",()=>{
                frm.set_value("status","Picked Up");
                frm.save();
            })
        }

        frm.add_custom_button("Cancel",()=>{
            let d = new frappe.ui.Dialog({
                title:"Cancel Reason",
                fields: [
                    {
                        label:"Cancellation Reason",
                        fieldname:"cancellation_reason",
                        fieldtype:"Small Text",
                        reqd:1
                    }
                ],
                primary_action_label:"Send",
                primary_action(values){
                    frappe.msgprint("Cancelled Successfully");
                    d.hide();
                }
            });
            d.show()
        })
        frm.add_custom_button("Reassign Attendant",()=>{
            frappe.prompt({
                label:"New Attendant",
                fieldname: 'attendant',
                fieldtype: 'Link',
                options:"Attendant",
                reqd:1
            }, (values) => {
                frappe.confirm("Are you sure want to confirm this reassign",()=>{
                    frappe.call({
                        method:"pawpass.pawpass.api.reassign_attendant",
                        args:{stay_card:frm.doc.name,attendant:values.attendant},
                        callback(r){
                            // frm.reload_doc();
                            frm.trigger("assigned_attendant");
                            frappe.msgprint("Attendant reassigned");
                        }
                    });
                });
            },"Reassign Attendant","Reassign");
        })
    }
});
