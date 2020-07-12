$('document').ready(function() {

    const ajax = $.ajax({
      type: "GET",
      url: "/search",
      dataType: "json"
    });

    const removeAccents = (str) => {
      return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
    } 

    const result = $('#result');
    const search = $('#search');

    $('#search').on('keyup', function() {

        result.html("");

        if (search.val() !== "") {

            result.show();
        } else {

            result.hide();
        }

        const datos = JSON.parse(ajax.responseText)

        const text = search.val().toLowerCase();
        
        for (let dato of datos.result) {

            let name = dato.name.toLowerCase();
            let name_normalize = removeAccents(name)

            if (name_normalize.indexOf(text) !== -1) {
                var item = document.createElement('a');
                item.classList = 'dropdown-item';
                item.href = "#";
                item.innerText = dato.name  
                result.append(item)
            }
        }

        if (result.html() === "") {
            var item = document.createElement('span');
            item.classList = 'dropdown-item';
            item.innerHTML = '<span>Sin resultados!</span>'
            result.append(item);
        }
    });
});