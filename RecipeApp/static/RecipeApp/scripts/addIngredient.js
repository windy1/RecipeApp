$(function() {
    $('#addIngredientBtn').click(function(e) {
        // TODO: this just lets you enter anything right now
        let text = $('#addIngredient').val().trim();
        $('#ingredients').append('<option>' + text + '</option>');
    });
});
