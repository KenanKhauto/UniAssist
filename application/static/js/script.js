$(document).on('click', '.dropdown', function() {
  $(this).toggleClass('open');
});

$(document).on('click', function(event) {
  if (!$(event.target).closest('.dropdown').length) {
    $('.dropdown').removeClass('open');
  }
});


window.onload = function () {
  bootlint.showLintReportForCurrentDocument([], {
      hasProblems: false,
      problemFree: false
  });

  $('[data-toggle="tooltip"]').tooltip();

  function formatDate(date) {
      return (
          date.getDate() +
          "/" +
          (date.getMonth() + 1) +
          "/" +
          date.getFullYear()
      );
  }

  var currentDate = formatDate(new Date());

  $(".due-date-button").datepicker({
      format: "dd/mm/yyyy",
      autoclose: true,
      todayHighlight: true,
      startDate: currentDate,
      orientation: "bottom right"
  });

  $(".due-date-button").on("click", function (event) {
      $(".due-date-button")
          .datepicker("show")
          .on("changeDate", function (dateChangeEvent) {
              $(".due-date-button").datepicker("hide");
              $(".due-date-label").text(formatDate(dateChangeEvent.date));
          });
  });
};


// Process the math elements in the document using MathJax
//MathJax.typesetPromise();
