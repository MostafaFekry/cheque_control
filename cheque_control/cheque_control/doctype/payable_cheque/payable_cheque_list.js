frappe.listview_settings['Payable Cheque'] = {
	add_fields: ["cheque_no", "status", "party", "party_name",
		"amount", "cheque_date"],
	filters: [["status", "!=", "Cheque Cancelled"]],
	get_indicator: function(doc) {
		if(doc.status==="Submitted") {
			return [__("Cheque Issued"), "Light Blue", "status,=,Submitted"];
		} else {
			return [__(doc.status), {
				"Draft": "red",
				"Cheque Cancelled": "red",
				"Cheque Issued": "lightblue",
				"Cheque Deducted": "green"
			}[doc.status], "status,=," + doc.status];
		}
	}
};