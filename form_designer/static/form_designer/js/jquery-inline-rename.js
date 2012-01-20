/*
Replaces the name in an inline element's header while typing it in the input of the "name" field.
This way, the extra inline element's header will be named instead of numbered #4, #5 etc.
*/

jQuery(function($) {

    var nameField = $.scriptUrlParam ? $.scriptUrlParam(/jquery-inline-rename\.js(\?.*)?$/, 'nameField', 'name') : 'name';
    var target = $('div.inline-group');
    var item = 'div.inline-related';
    var nameInput = 'input[id*=-'+nameField+']';
    
    var init = function() {
        target.find(item).each(function() {
            var input = $(this).find(nameInput);
            var label = $('.inline_label', this);
            var rename = function(evenIfEmpty) {
                if (evenIfEmpty || input.val()) {
                    label.text(input.val());
                }
            };
            input.keyup(function(event) {
                // Update name while typing
                rename(true);    
            });
            rename(false);
        })
    }
    
    init();
    // init again when "Add another" link is clicked
    $('.add-row a').click(function() {
        init();
    })
});
