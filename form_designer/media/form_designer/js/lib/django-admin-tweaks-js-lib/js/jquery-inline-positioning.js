/*
Enables positioning of the inline elements by drag & drop.

All the inline model requires is a "position" field that is blank by default.
This value will be set automatically by this code snippet when dragging elements.
The model can then be ordered by "position".
*/

jQuery(function($) {
	
	var positionField = $.scriptUrlParam ? $.scriptUrlParam(/jquery-inline-positioning\.js(\?.*)?$/, 'positionField', 'position') : 'position';
	var target = $('div.inline-group');
	var handle = 'h3 b';
	var item = 'div.inline-related';
	var positionInput = 'input[id$=-'+positionField+']';

	target.find(item).each(function(i) {
		$(this).find(handle).css('cursor', 'move');
		$(this).find(handle).addClass('draggable');
		$(this).find(positionInput).each(function() {
			$(this)[0].readOnly = true;
		});
		$(this).find('input, select, textarea').change(function() {
			$(this).closest(item).find('input[id$='+positionField+']').val('X'); // mark for renumberAll() to fill in
			renumberAll($('div.inline-group'));
		});
	});

	var renumberAll = function() {
		target.find(item).each(function(i) {
			if ($(this).find(positionInput).val() != '') {
				$(this).find(positionInput).val(i+1);
			}
		});
	};

	target.sortable({
		containment: 'parent',
		/*zindex: 10, */
		items: item,
		handle: handle,
		update: renumberAll,
		opacity: .75
	});
});
