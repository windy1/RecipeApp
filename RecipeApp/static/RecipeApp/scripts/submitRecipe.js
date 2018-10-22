$(function() {
    $('#addIngredient').click(function() {
        let ingCount = $('#ingredients > .form-row').length;
        let ingNum = ingCount + 1;
        let ing = $('#ingredient').clone().attr('id', 'ingredient' + ingNum).removeAttr('style');
        ing.find('#quantity').attr('id', 'quantity' + ingNum).attr('name', 'quantity' + ingNum);
        ing.find('#ingName').attr('id', 'ingName' + ingNum).attr('name', 'ingName' + ingNum);
        bindRemoveBtn(ing.find('.btn-remove-recipe'));
        $('#ingredients').append(ing);
    });

    $('#addDirection').click(function() {
        let dirCount = $('#directions > .form-row').length;
        let dirNum = dirCount + 1;
        let dir = $('#direction').clone().attr('id', 'direction' + dirNum).removeAttr('style');
        dir.find('#dirText').attr('id', 'dirText' + dirNum).attr('name', 'dirText' + dirNum);
        bindRemoveBtn(dir.find('.btn-remove-dir'));
        $('#directions').append(dir);
    });
});

function bindRemoveBtn(e) {
    e.click(function() {
        $(this).closest('.form-row').remove();
    });
}
