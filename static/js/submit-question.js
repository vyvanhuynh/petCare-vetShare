'use strict';


$('#question_form').on('submit', evt => {
  evt.preventDefault();

  const myFile = $('input[name="images-file"]')[0].files[0];
  const questionBody = $('#new-question').val();
  if (myFile != undefined) {
    
    const formData = new FormData();
    formData.append('images-file', myFile);
    formData.append('new-question', questionBody);
    $.ajax({
        url: '/submit_question',
        data: formData,
        processData: false,
        contentType: false,
        type: 'POST',
        success: res => {
            alert(res);
            document.getElementById("question_form").reset();
            $( "#quesans" ).load(window.location.href + " #quesans" );
            // Add your fancy JavaScript here.
        }
    });
  }
  else {
      const formData = new FormData();
      formData.append('new-question', questionBody);
      $.ajax({
        url: '/submit_question',
        data: formData,
        processData: false,
        contentType: false,
        type: 'POST',
        success: res => {
            alert(res);
            document.getElementById("question_form").reset();
            $( "#quesans" ).load(window.location.href + " #quesans" );
            // Add your fancy JavaScript here.
        }
    });
  }

});