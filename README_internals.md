### B2c

self.save() should not use inside th validate() because as when we call self.save() inside validate(), the self.save() will call the validate in loop. Becaue in general when we call save() by default it will call validate()

Corrected Code:

def validate(self):  
    self.services_total = sum(r.line_total for r in self.service_lines)  

Updating pet everytime when the validate calls so in general we can call multiple time validate finction so in ecah time it will update the stay value. But we need to update the value not everytime just one time we need to apply only when it insert or save (only once not everytime)

def after_insert(self):
    pet = frappe.get_doc("Pet", self.pet)  
    pet.total_stays += 1  
    pet.save()


### B2d

This error occurs when multiple user access the same document , when the one user changes the document while you save . It uses optimistic locking to check whether the document was changed before you save it and it will stop when the change occurs.

### C3

assigned_attendant on Stay cards will updates automatically, since it is a link field and Frappe syncs all linked references on rename.We can rename either bu ui rename button or by frappe.rename.doc()


### D2

In frappe.get_all it doesnt check with the permission , but when we use frappe.get_list() it will work with permission so ,frappe.get_all() has low_previlage in whitelisted API


### E1

We should not call self.save() inside update() because when we call save it will check validate, update . So it will recursively call.

def on_update(self):
    self.db_set("status", "Processed")


### E2

When we give merge=false it will show an error that the name already exists and if we give merge=true it doest check and it will override nthe existing document.

### E3

days = frappe.db.get_value("PawPass Settings", None, "reminder_days_before_checkout")

This is the correct pattern, as 

### H1

Fetch the data early (in onload or refresh) and store it, then check that stored value inside validate (no waiting needed).
Or do the real check in the server-side Python validate(), since that runs safely as part of the actual save process and can talk to the database directly.
Never depend on frappe.call inside client-side validate it is async and returns after validate already finished, so the save isn't actually blocked. Fetch data ahead of time in onload/refresh and cache it, or do the real check in the server-side validate() method."


### I1

we should not build SQL with f-strings when using user input always use %s with the parameter values, so input store as data and it will turn into SQL commands

### J1

we should not call frappe.get_all() inside a jinja print template it skips to check the permission and mixes logic with display. We can work it in before_print() instead, store on doc.precomputed_field, and let the template just read it.

### L1

API/RESOURCE

suba@Suba:~/frappe-bench-v16$ curl http://127.0.0.1:8000/api/resource/Stay%20Card -H "Authorization: token ad12cd0226aac58:1eb6576a94ab573"
{"data":[{"name":"PC-2026-00009"},{"name":"PC-2026-00010"}]}suba@Suba:~/frappe-bench-v16$ 

Valid URL (with correct document name):

http://127.0.0.1:8000/api/method/pawpass.pawpass.api.get_stay_summary?stay_card_name=PC-2026-00010

{
  "message": {
    "name": "PC-2026-00010",
    "pet code": "PET-2026-0002",
    "owner name": "Anu",
    "final amount": 4000,
    "email": "anu@gmail.com"
  }
}

Wrong Path with invalid stay card document:

http://127.0.0.1:8000/api/method/pawpass.pawpass.api.get_stay_summary?stay_card_name=PC-2026-000101

{
  "message": {
    "error": "Not Found"
  }
}

Post Method:

suba@Suba:~/frappe-bench-v16$ curl -X POST "http://127.0.0.1:8000/api/resource/Stay%20Card" -H"Authorization: token ad12cd0226aac58:1eb6576a94ab573" -H "Content-Type: application/json" -d '{"pet":"PET-2026-0002","checkin_date":"2026-09-25"}'

Output:

{"data":{"name":"PC-2026-00012","owner":"Administrator","creation":"2026-09-25 16:36:51.041968","modified":"2026-09-25 16:36:51.041968","modified_by":"Administrator","docstatus":0,"idx":0,"workflow_state":"Draft","pet":"PET-2026-0002","owner_name":"Anu","owner_phone":"8122458941","checkin_date":"2026-09-25","purpose":"Grooming Only","vaccination_status":"Valid","services_total":0.0,"fianl_amount":0.0,"payment_status":"Unpaid","status":"Draft","doctype":"Stay Card","service_lines":[]}}suba@Suba:~/frappe-bench-v16$ 

### K2

in the given code the method get_doc() is inside loop, which will call the db multiple times, if we have n documents, it will call trhe db n+1 times, but we can reduce it to just 2 calls using the below fixed code:

def attendants_detail():
        stay_cards = frappe.get_all(
            "Stay Card",
            fields=["name", "assigned_attendant"]
        )
        attendant_names=[]
        for s in stay_cards:
            attendant_names.append(s.assigned_attendant)
        attendants = frappe.get_all(
            "Attendant",
            filters={
                "name": ["in", attendant_names]
                },
            fields=["name", "attendant_name", "phone"]
        )
        for attendant in attendants:
            print(attendant.attendant_name, attendant.phone)

### Screen Recording Video link for this App

### https://drive.google.com/file/d/1Wna0jQ9AP-2QybheV9HZu7N53i0RrMWl/view?usp=sharing

### Script Report image

### https://drive.google.com/file/d/1qyWDyPBouzqE_poP-g0XsApQ2GeEhn13/view?usp=sharing 

### Print Format image

### https://drive.google.com/file/d/1PSLqvCpY8Tt4YFgE-4xaMUcVqD5MTpgr/view?usp=sharing