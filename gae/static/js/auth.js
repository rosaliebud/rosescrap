var auth = {
    session: null,
    init: function() {
        // get login status initially
        FB.getLoginStatus(function(response) {
            auth.onSessionChange(response);
            // listen to future changes
            FB.Event.subscribe('auth.sessionChange', auth.onSessionChange);
        });
    },
    onSessionChange: function(response) {
        if (response.session) {
            $('div#logged-out').hide();
            // logged in and connected user, someone you know
            auth.session = response.session;
            $('#fb-profile-pic').attr('uid', auth.session.uid);
            $('#fb-name').attr('uid', auth.session.uid);
            FB.XFBML.parse($('div#logged-in')[0], function() {
                $('div#logged-in').show();
            });
        } else {
            // no user session available, someone you dont know
            auth.session = null;
            $('div#logged-in').hide();
            FB.XFBML.parse($('div#logged-out')[0], function() {
                $('div#logged-out').show();
            });
        }
    }
};

$(function(){
    auth.init();
});
