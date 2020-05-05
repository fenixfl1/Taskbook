function notifications() {

    $.ajax({
        url: "/notications",
        type: "POST",
        processData: "data",
        dataType: "aplication/json",
        success: function (data) {
            $("#notification-count").remove();                                      
            $("#notification-latest").show();$("#notification-latest").html(data);
        },
        errro: function() {}
    });
}

$(document).ready(function () {
    
    $('body').click(function(e) {
        if ( e.target.id != 'notification-icon'){
            $("#notification-latest").hide();
        }
    })
});