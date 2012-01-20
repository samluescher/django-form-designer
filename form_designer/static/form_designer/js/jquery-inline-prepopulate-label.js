/*
Does exactly what `prepopulated_fields = {"label" : ('name',)}`
would do, but does not URLify the value (since in this case, name is a slug field 
but label is a title field).
*/

jQuery(function($) {

    var target = $('div.inline-group');
    var item = 'div.inline-related';
    var labelSel = 'input[id*=-label]';
    var nameSel = 'input[id*=-name]';

    var init = function() {
        $(target).find(item).each(function(i) {
            var item = $(this);
            item.find(labelSel).each(function() {
                this._changed = item.find(nameSel).val() != $(this).val();  
            });
            item.find(labelSel).change(function() {
                this._changed = true;  
            });
            item.find(nameSel).keyup(function() {
                labelInput = item.find(labelSel);
                if (!labelInput[0]._changed) {
                    labelInput.val($(this).val());
                }
            });
        });
    }

    init();
    // init again when "Add another" link is clicked
    $('.add-row a').click(function() {
        init();
    })
});