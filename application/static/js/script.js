$(document).on('click', '.dropdown', function() {
  $(this).toggleClass('open');
});

$(document).on('click', function(event) {
  if (!$(event.target).closest('.dropdown').length) {
    $('.dropdown').removeClass('open');
  }
});

// Process the math elements in the document using MathJax
//MathJax.typesetPromise();
