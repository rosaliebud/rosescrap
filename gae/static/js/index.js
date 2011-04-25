$(function(){
    var listForm = $('form#list');
    listForm.submit(function() {
        // make sure form is filled out
        if (!this[0].value.length) {
            alert('no name!');
            return false;
        }
        if (!this[1].files.length) {
            alert('no photo!');
            return false;
        }

        // check to see if user is logged in
        if (auth.session) {
          return true;
        } else {
            FB.login(function(response) {
                if (response.session) {
                    listForm.submit();
                } else {
                    alert('must be logged in to list');
                }
            });
            return false;
        }
    });
});
