// $(document).ready(function(){
//     var files;
//     $('input[type=file]').on('change', prepareUpload);


//     function prepareUpload(e){
//         files =  e.target.files;
//     }
//     $('#upload').on('click', uploadFiles);

//     function uploadFiles(e){
//         var data = new FormData();
//         $.each(files, function(key,value){
//             data.append(key, value);
//         });

//         $.ajax({
//             url: 'upload.php',
//             type: 'POST',
//             data: data,
//             cache: false,
//             dataType: 'json',
//             contentType: false,
//             success: function(data, status, jqXHR){
//                 if(typeof data.error == 'undefined'){
//                     sub////////////////edit
//                 }
//             },
//             error: function(jqXHR, status, error){
//                 console.log(status)
//             }
//         });

//     }


// });