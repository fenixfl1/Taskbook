function mostrar() {
    var archivo = document.getElementById("file").files[0];
    var reader = new FileReader();
    if (file) {
        reader.readAsDataURL(archivo);
        reader.onloadend = function() {
            document.getElementById("img").src = reader.result;
        }
    }
}


// add id='filechooser' in the input type file 
function uploadFile() {
    var blobFile = $('#filechooser').files[0];
    var formData = new FormData();
    formData.append("fileToUpload", blobFile);

    $.ajax({
        url: "upload.php",
        type: "POST",
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            // .. hacer algo...
        },
        error: function(jqXHR, textStatus, errorMessage) {
            console.log(errorMessage); // Opcional
        }
    });
}