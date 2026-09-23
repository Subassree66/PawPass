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
    // refresh(frm){
    //     if(frm.doc.status=="Ready for Pickup" AND docstatus==1)
            
    // }
    refresh(frm){
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
                fieldtype: 'Data'
            }, (values) => {
                frappe.msgprint(values.attendant);
            })
        })
    }
});
