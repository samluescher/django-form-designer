/*
Does exactly what 
  prepopulated_fields = {"label" : ('name',)}
would do, but does not URLify the value (since in this case, name is a slug field but label is a title field)
*/


jQuery(function($) {

	var target = $('div.inline-group');
	var item = 'div.inline-related';

	$(target).find(item).each(function(i) {
	    var item = $(this);
        item.find('input[id*=-label]').each(function() {
	        this._changed = item.find('input[id*=-name]').val() != $(this).val();  
	    });
        item.find('input[id*=-label]').change(function() {
	        this._changed = true;  
	    });
        item.find('input[id*=-name]').keyup(function() {
	        labelInput = item.find('input[id*=-label]');
	        if (!labelInput[0]._changed) {
	            labelInput.val($(this).val());
	        }
	    });
	});

});