WATSAN.ProjectTemplate = _.template("" +
	"<div class='project' id='<%= id %>'>" +
		"<div class='project-steps'>" +
			"<table>" +
				"<tr class='step _1'>" +
					"<td>" +
						"<h4>Step 1: Find Potential Site(s)</h4>" +
						"<p>Add sites to the map to view estimated costs</p>" +
					"</td>" +
					"<td><a href='/watsan/map/<%= id %>' class='button'>View Map<span class='typicn typcn-map'></span></a></td>" +
				"</tr>" +
				"<tr class='step _2 incomplete'>" +
					"<td colspan='2'>" +
						"<h4>Step 2: Compare Potential Site(s)</h4>" +
					"</td>" +
				"</tr>" +
				"<tr class='step _2 incomplete'>" +
					"<td colspan='2'>" +
						"<div class='site-table'>"+
							"<table class='table'>" +
								"<thead>"+
			                        "<tr>"+
			                            "<th>Name</th>"+
			                            "<th>Pilot Area</th>"+
			                            "<th>Sewer</th>"+
			                            "<th>Water</th>"+
			                            "<th>Landmarks</th>"+
			                        "</tr>"+
			                    "</thead>"+
								"<tbody>"+
									"<tr class='no-sites'><td>You haven't chosen any sites yet</td></tr>" +
								"</tbody>"+
							"</table>"+
						"</div>" +
					"</td>" +
				"</tr>" +
				"<tr class='step _3 incomplete'>" +
					"<td>" +
						"<h4>Step 3: Connect to Nairobi Water or an Alternative</h4>" +
						"<p>Click the buttons below to get more details</p>" +
					"</td>" +
					"<td><a class='button' href='http://www.nairobiwater.co.ke/contact_us/?ContentID=2' target='_blank'>View Contact Info</a></td>" +
				"</tr>" +
			"</table>" +
		"</div>" +
	"</div>")