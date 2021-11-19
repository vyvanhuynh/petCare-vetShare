'use strict';

$('#answer_form').on('submit', evt => {
  evt.preventDefault();

  const formInputs = {
    answerBody: $('#new-answer').val(),
  };

  $.post('/submit_answer', formInputs, res => {
    alert(res);
    document.getElementById("answer_form").reset();
    $( "#quesans" ).load(window.location.href + " #quesans" );
  });
});