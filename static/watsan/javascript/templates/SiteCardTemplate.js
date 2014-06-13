WATSAN.SiteCardTemplate = _.template("" +
	"<div id='site-<%= cid %>' class='card <%= color %>'>" +
		"<a class='alert delete typicn typcn-delete-outline'></a>" +
		"<input id='input-<%= cid %>' class='name_input' data-id='<%= cid %>' value='<%= name %>'>"+
		"<div class='card-details'><table>" +
			"<tr class='<% if (sewer_status.connect != 'False') { %> text-left <% } else { %> trans-red <% } %>'>"+
				"<td class='label'>Sewer: </td>" +
				"<td class='answer'><% if(sewer_status.connect != 'False') { %>"+
					" Est. <%= _.numberFormat(parseFloat(sewer_status.cost)) %>/=KSH,<br />"+
					" <%= _.numberFormat(parseFloat(sewer_status.distance)) %> meters"+
				"<% } else { %>"+
					" Not possible"+
				"<% } %> </td>"+
			"</tr>"+
			"<tr class='<% if (water_status.connect != 'False') { %> text-left <% } else { %> trans-red <% } %>'>"+
				"<td class='label'>Water:</td>" +
				"<td class='answer'><% if(water_status.connect != 'False') { %>"+
					" Est. <%= _.numberFormat(parseFloat(water_status.cost)) %>/=KSH,<br />"+
					" <%= _.numberFormat(parseFloat(water_status.distance)) %> meters"+
				"<% } else { %>"+
					" Not possible"+
				"<% } %> </td>"+
			"</tr>"+
			"</table>" +
			"<div class='hide extra'><table>" +
			"<tr><td class='label'>Area:</td><td class='answer'><%= pilot_area %></td></tr>"+
			"<tr class='text-left'>"+
				"<td class='label'>Near:</td>" +
				"<td class='answer'><%= nearby %>"+
			"</tr>" +
			"<tr><td class='label'>Lat:</td><td class='answer'>" +
				"<%= _.numberFormat(parseFloat(latlong.lat), 5) %></td></tr> " +
			"<tr><td class='label'>Lng:</td><td class='answer'>" +
				"<%= _.numberFormat(parseFloat(latlong.lng), 5) %>" +
			"</td></tr>" +
		"</table></div>" +
		"<div class='more closed'>More Detail</div>" +
		"</div>" +
	"</div>")