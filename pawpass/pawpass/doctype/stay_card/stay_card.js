// Copyright (c) 2026, Suba and contributors
// For license information, please see license.txt

frappe.ui.form.on("Stay Card", {
	setup(frm) {
        frm.set_query("assigned_attendant",()=>{
            let is_boarding =(frm.doc.purpose || "").includes("Boarding");
            return{
                filters:{
                    status:"Active",
                    "specialization.is_boarding":is_boarding?1:0
                }
            };
        });

    },

    refresh(frm){
        if(frm.doc.status=="Ready for Pickup"){
            frm.dashboard.add_indicator ("Ready for Pickup","orange");
        }
        else if(frm.doc.status=="Draft"){
            frm.dashboard.add_indicator("Draft","purple")
        }
        else if(frm.doc.status=="Cancelled"){
            frm.dashboard.add_indicator("Cancelled","black")
        }
        else if(frm.doc.status=="Picked Up"){
            frm.dashboard.add_indicator("Picked Up","green")
        }
        else if(frm.doc.status=="Checked In"){
            frm.dashboard.add_indicator("Checked In","red")
        }
        else{
            frm.dashboard.add_indicator(frm.doc.status,"blue")
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

frappe.ui.form.on("Service Line",{
    quantity(frm,cdt,cdn){
        let row=locals[cdt][cdn];
        let total=(row.rate||0)*(row.quantity||0);
        frappe.model.set_value(cdt,cdn,"line_total",total).then(()=>{
            calculate_service_total(frm);
        });
    }
});
function calculate_service_total(frm){
    let total=0;
    (frm.doc.service_linees || []).forEach(row =>{
        total+=row.line_total||0;
    });
    frm.set_value("services_total",total);
    frm.set_value("fianl_amount",total);
}
