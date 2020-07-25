function countDown (selector) {

    var top = document.getElementById('dia-entrega');

    const topDate = new Date(top.value);

    const updateClock = (date) => {
        if (!date) return;

        let end = date.getTime();
        let now = Date.now();
        let diff = end - now;

        let days = Math.floor(diff / 86400000);
        diff = diff % 86400000;

        let hours = Math.floor(diff / 3600000);
        diff = diff % 3600000;

        let minutes = Math.floor(diff / 60000);
        diff = diff % 60000;

        let seconds = Math.floor(diff / 1000);
        
        document.getElementById('date').innerHTML = days + "D -" + hours + "H -" + minutes + "M -" + seconds + "s";
    }

    updateClock(topDate);

    setInterval(updateClock, 1000, topDate)
}


$(document).ready(function() {

    const cards = $('.card').each(function (index) {

        $(this).find('#date').append($(this).find('.fecha').val()); 
    });
    
    // countDown();
});