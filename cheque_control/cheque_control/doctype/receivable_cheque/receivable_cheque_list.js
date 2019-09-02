frappe.listview_settings['Receivable Cheque'] = {
	add_fields: ["cheque_no", "status", "party", "party_name",
		"amount", "cheque_date"],
	filters: [["status", "!=", "Cheque Cancelled"]],
	get_indicator: function(doc) {
		if(doc.status==="Submitted") {
			return [__("Cheque Received"), "Light Blue", "status,=,Submitted"];
		} else {
			return [__(doc.status), {
				"Draft": "red",
				"Cheque Cancelled": "red",
				"Cheque Received": "lightblue",
				"Cheque Deposited": "orange",
				"Cheque Rejected": "red",
				"Cheque Returned": "darkgrey",
				"Cheque Collected": "green"
			}[doc.status], "status,=," + doc.status];
		}
	}
};