
const search = document.querySelector("#search");

const result = document.querySelector('#resultado');

const xhttp = new XMLHttpRequest();

xhttp.open('GET', '/search_courses', true);

xhttp.send();

alert('before the filter function')

const filter = () => {

    alert('into the filter function')

    result.innerHTML = "";

    const datos = JSON.parse(xhttp.responseText);

    const text = search.value.toLowerCase();

    for (let course of datos) {
        let name = course.name.toLowerCase();

        // var item = document.createElement("a");

        // item.classList.add("dropdown-item");
        // item.href = "#"
        // item.innerText = course.name
        
        if (name.indexOf(text) !== -1) {
            result.innerHTML += `<li>${course.name}</li>`
        }
    }

    if (result.innerHTML === '') {
        result.innerHTML += `
            <li>Sin resultados</li>
        `
    }
}

search.addEventListener('keyup', filter);