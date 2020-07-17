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
            let table_name = dato.table_name.toLowerCase();

            let name_normalize = removeAccents(name)
            let tm_normalize = removeAccents(table_name)

            if (name_normalize.indexOf(text) !== -1  || tm_normalize.indexOf(text) !== -1) {
                var item = document.createElement('a');
                item.classList = 'dropdown-item';
                item.innerText = dato.name

                if (dato.table_name === "courses") {
                    item.href = "/courses/" + dato.id
                } 

                else if (dato.table_name === "teachers") {
                    item.href = "/teachers/" + dato.id
                }

                else if (dato.table_name === "study-plan") {
                    item.href = "/studies-plan/" + dato.id
                }

                else if (dato.table_name === 'users') {
                    item.innerText = dato.name + " " + dato.user_id
                    url = '/users/' + dato.id + "/" + dato.name + "/"
                    item.href = url
                }

                else {
                    item.href = "/tasks/details/" + dato.id
                }

                result.append(item)
            }
        }

        if (result.html() === "") {
            var item = document.createElement('span');
            item.classList = 'dropdown-item';
            item.innerHTML = '<span class="text-warning">Sin resultados!</span>'
            result.append(item);
        }
    });
});