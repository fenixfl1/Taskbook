function countDown () {

    var top = document.getElementById('dia-entrega');

    var current_date = Date.UTC(top.value)

    console.log(current_date)

    const topDate = new Date(current_date);

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
        
        document.getElementById('date').innerHTML = days + "" + hours + "" + minutes + "" + seconds;
    }

    updateClock(topDate);

    setInterval(updateClock, 1000, topDate)
}


$(document).ready(function() {
    
    countDown();
});