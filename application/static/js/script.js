$(document).on('click', '.dropdown', function() {
  $(this).toggleClass('open');
});

$(document).on('click', function(event) {
  if (!$(event.target).closest('.dropdown').length) {
    $('.dropdown').removeClass('open');
  }
});