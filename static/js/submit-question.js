'use strict';

$('#question_form').on('submit', evt => {
  evt.preventDefault();

  const formInputs = {
    questionBody: $('#new-question').val(),
  };

  $.post('/submit_question', formInputs, res => {
    alert(res);
    document.getElementById("question_form").reset();
    $( "#quesans" ).load(window.location.href + " #quesans" );
  });
});
