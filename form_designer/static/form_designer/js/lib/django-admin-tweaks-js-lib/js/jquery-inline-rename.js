/*
Replaces the name in an inline element's header while typing it in the input of the "name" field.
This way, the extra inline element's header will be named instead of numbered #4, #5 etc.
*/

jQuery(function($) {

	var nameField = $.scriptUrlParam ? $.scriptUrlParam(/jquery-inline-rename\.js(\?.*)?$/, 'nameField', 'name') : 'name';
	var target = $('div.inline-group');
	var item = 'div.inline-related';
	var containsName = 'h3';
	var beforeName = 'h3 > *:first';
	var afterName = 'h3 > *:last';
	var nameInput = 'input[id*=-'+nameField+']';
	
	target.find(item).each(function() {
		// The following code is due to the fact that  the inline 
		// element's name is (lamentably) not wrapped in a tag. 

		// 1. Strip everything before and after name
		var stripBefore = $(this).find(beforeName).remove();
		var stripAfter = $(this).find(afterName).remove();
		// 2. Now we can get the name (text node)
		var nameParent = $(this).find(containsName);
		var name = $(nameParent).html();
		// 3. Strip leading whitespace including &nbsp;
		name = name.replace( /^(\s|&nbsp;)+/g, "" )
		// 4. Wrap name in tag
		name = $('<span>'+name+'</span>');
		// 5. Re-insert it with a space before
		$(nameParent).html(name);
		$(name).before('&nbsp;');
		// 6. Restore everything before and after name
		$(nameParent).prepend(stripBefore);
		$(nameParent).append(stripAfter);
		
		// Update name while typing
		$(this).find(nameInput).keyup(function(event) {
			name.html($(this).val());
		})
	})
	

});
