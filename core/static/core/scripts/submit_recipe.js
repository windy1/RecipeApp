$(function() {
    $('#add_ingredient').click(function() {
        /**
         * Event when a new ingredient should be added to the list
         * @type {jQuery}
         */
        let ing_count = $('#ingredients > .form-row').length;
        let ing_num = ing_count + 1;
        let ing = $('#ingredient').clone().attr('id', 'ingredient' + ing_num).removeAttr('style');
        let ing_name = ing.find('#ing_name');
        ing.find('#quantity').attr('id', 'quantity' + ing_num).attr('name', 'quantity' + ing_num);
        ing_name.attr('id', 'ing_name' + ing_num).attr('name', 'ing_name' + ing_num);
        bind_remove_btn(ing.find('.btn-remove-recipes'));
        bind_ingredient_lookup(ing_name);
        $('#ingredients').append(ing);
    });

    $('#add_direction').click(function() {
        /**
         * Event when a new direction should be added to the list
         * @type {jQuery}
         */
        let dir_count = $('#directions > .form-row').length;
        let dir_num = dir_count + 1;
        let dir = $('#direction').clone().attr('id', 'direction' + dir_num).removeAttr('style');
        dir.find('#dir_text').attr('id', 'dir_text' + dir_num).attr('name', 'dir_text' + dir_num);
        bind_remove_btn(dir.find('.btn-remove-dir'));
        $('#directions').append(dir);
    });
});

function bind_remove_btn(e) {
    e.click(function() {
        $(this).closest('.form-row').remove();
    });
}

function bind_ingredient_lookup(e) {
    e.on('input', function() {
       let name = e.val();
       console.log(name);
    });
}
