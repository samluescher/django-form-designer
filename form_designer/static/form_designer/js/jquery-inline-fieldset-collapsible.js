/*
Makes all fieldsets inside of inline forms collapsible.
*/

jQuery(function($) {
    var init = function() {
        $('div.inline-related').each(function(i) {
            $.makeCollapsible(this, 'fieldset', '.form-row', 'h2', null, true)
        });
    };

    init();
    // init again when "Add another" link is clicked
    $('.add-row a').click(function() {
        init();
    })
});
