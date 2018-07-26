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


$(document).ready(function() { 
    console.log('ready');
    var options = { 
        target:   '#output',    
        beforeSubmit:  beforeSubmit,   
        success:       afterSuccess,
        resetForm: true         
    }; 
    $('#fileupload').submit(function() { 
        $(this).ajaxSubmit(options);                
        return false; 
    }); 

    var request;
    $('#textbox').on('submit', function(e){
        console.log("reached textbox");
        e.preventDefault();
        var sentNum = $('#sentNum').val()
        var text = $('#textarea').val()
        console.log(sentNum);
        console.log(text);
        $.ajax({
            url: '/summarize',
            type: 'post',
            contentType: 'application/json; charset=utf8',
            dataType: 'json',
            data: JSON.stringify({
                type: 'text',
                num: sentNum,
                data: text
            }),
            success: function(data){
                // highlight the text returned
                console.log(data.og)
                console.log(data.summary)
                $("#highlighttext").text(data.og)
                summaryString = ""
                $("#textsummary").text("")
                for(i = 0; i<data.summary.length; i++){
                    $("#textsummary").append("<li>" + data.summary[i] + "</li>")
                }
                return "blah"
            },
            error: function(error){
                return "error"
            }
        });
        return "blah"
    });

    $('#externalurl').on('submit', function(e){
        e.preventDefault();
        var sentNum = $('#sentNum').val()


    });
        
    function afterSuccess(){
        console.log("successful file upload")
    }

            
    function beforeSubmit(){
        if (window.File && window.FileReader && window.FileList && window.Blob){
            if( !$('#file').val()) {
                $("#output").html("No file selected.");
                return false;
            }
        
            var fsize = $('#file')[0].files[0].size; 
            var ftype = $('#file')[0].files[0].type; 

            //allow file types 
            switch(ftype){
                case 'image/png': 
                case 'image/jpeg': 
                case 'image/pjpeg':
                case 'application/pdf':
                case 'application/msword':
                case 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                case 'text/plain':
                case 'text/html':
                case 'application/epub+zip':
                    break;
                default:
                    $("#output").html("<b>"+ftype+"</b> Unsupported file type!");
                    return false
            }
        
            //Allowed file size is less than 50 MB (1MB: 1048576)
            if(fsize>52428800){
                $("#output").html("<b>"+bytesToSize(fsize) +"</b> Too big file! <br />File is too big, it should be less than 50 MB.");
                return false;
            }
                
            // $("#output").html("");  
        }
        else{
            //Output error to older unsupported browsers that doesn't support HTML5 File API
            $("#output").html("Please upgrade your browser, because your current browser lacks some new features we need!");
            return false;
        }
    }

    //function to format bites bit.ly/19yoIPO
    function bytesToSize(bytes) {
        var sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
        if (bytes == 0) return '0 Bytes';
        var i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
        return Math.round(bytes / Math.pow(1024, i), 2) + ' ' + sizes[i];
    }

}); 
