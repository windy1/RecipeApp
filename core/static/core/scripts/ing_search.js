$(function() {
    $('.btn-add-ing').click(function() {
        let e = $('<li class="list-group-item ing-item"><input class="form-control" type="text"></li>');
        e.insertBefore($('.item-add-ing'));
    });

    $('.ing-search-form').submit(function(e) {
        let hiddenIn = $(this).find('#ingredients');
        let inputs = $('.ing-list .ing-item');
        let len = inputs.length;
        hiddenIn.val('');

        inputs.each(function(i) {
            let ing = $(this).find('input');
            hiddenIn.val(hiddenIn.val() + ing.val());
            if (i < len - 1) hiddenIn.val(hiddenIn.val() + ',');
        });
    });
});
