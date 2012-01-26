/*
Enables repositioning of all inline elements by drag & drop.

The inline model requires is a "position" field that is blank by default.
This value will be set automatically by this code snippet when dragging elements.
The model instances can then be ordered by that "position" field.
*/

jQuery(function($) {
    
    var positionField = $.scriptUrlParam ? $.scriptUrlParam(/jquery-inline-positioning\.js(\?.*)?$/, 'positionField', 'position') : 'position';
    var target = $('div.inline-group');
    var handle = 'h3 b';
    var item = 'div.inline-related';
    var positionInput = 'input[id$=-'+positionField+']';
    var hidePositionFieldClosest = '.form-row';

    var renumberAll = function() {
        var pos = 1;
        target.find(item).each(function(i) {
            if ($(this).find(positionInput).val() != '') {
                $(this).find(positionInput).val(pos);
                pos++;
            }
        });
    };

    var init = function() {
        target.find(item).each(function(i) {
            if ($(this).data('isSortable')) return;
            $(this).data('isSortable', true);
        
            $(this).find(handle).css('cursor', 'move');
            $(this).find(handle).addClass('draggable');
            $(this).find(positionInput).each(function() {
                if (hidePositionFieldClosest) {
                    var hidden =$('<input type="hidden" id="'+this.id+'" name="'+this.name+'" />');
                    hidden.val($(this).val());
                    $(this).closest(hidePositionFieldClosest).replaceWith(hidden);    
                }
            });
            $(this).find('input, select, textarea').change(function() {
                $(this).closest(item).find('input[id$='+positionField+']').val('X'); // mark for renumberAll() to fill in
                renumberAll($('div.inline-group'));
            });
        });
    }

    var addRow = target.find('.add-row');
    addRow.remove();
    var ordered = [];
    var unordered = [];
    // Initially, remove and re-append all inlines ordered by their "position" value
    target.find(item).each(function(i) {
        var initialPos = $(this).find(positionInput).val();
        if (initialPos) {
            while (initialPos < ordered.length && ordered[initialPos]) {
                initialPos++;
            }
            ordered[initialPos] = this;
        } else {
            unordered[unordered.length] = this;
        }
        this.parentElement.removeChild(this);
    });
    for (var i = 0; i < ordered.length; i++) {
        var el = ordered[i];
        if (el) {
            target.append(el);
        }   
    }
    // Add "position"-less elements in the end
    for (var i = 0; i < unordered.length; i++) {
        var el = unordered[i];
        target.append(el);
    }
    target.append(addRow);

    target.sortable({
        containment: 'parent',
        /*zindex: 10, */
        items: item,
        handle: handle,
        update: renumberAll,
        opacity: .75
    });

    init();
    // init again when "Add another" link is clicked
    $('.add-row a').click(function() {
        init();
    })

});
