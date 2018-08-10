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

    // var options = { 
    //     target:   '#output',    
    //     beforeSubmit:  beforeSubmit,   
    //     success:       afterSuccess,
    //     resetForm: true         
    // }; 


$(document).ready(function() { 

    ////////////////////////////////Stuff for TinyMCE editable textbox////////////////

    $('#textsummary').tinymce({
        script_url: 'static/tinymce.min.js',
        plugins: 'autoresize lists'
        
    });
    $('#highlighttext').tinymce({
        script_url: 'static/tinymce.min.js',
        toolbar: false,
        menubar:false,
        statusbar:false,
        plugins: 'autoresize'
    });

    /////////////////////////////////////////////////////////////////////////////////

    function highlight(e){
        alert("hello")
    }

    $('#fileupload').show();
    $('#textbox').hide();
    $('#externalurl').hide();

    $('#gotoupload').click(function(e){
        $('#textbox').fadeOut(function(){
            $('#fileupload').fadeIn('slow');
        });
        $('#externalurl').fadeOut(function(){
            $('#fileupload').fadeIn('slow');
        });
        
    });
    $('#gototext').click(function(e){
        $('#fileupload').fadeOut(function(){
            $('#textbox').fadeIn('slow');
        });
        $('#externalurl').fadeOut(function(){
            $('#textbox').fadeIn('slow');
        });
    });
    $('#gotourl').click(function(e){
        $('#fileupload').fadeOut(function(){
            $('#externalurl').fadeIn('slow');
        });
        $('#textbox').fadeOut(function(){
            $('#externalurl').fadeIn('slow');
        });
    });

    var files;
    $('#file').on('change', function(event) { 
        files = event.target.files;
    }); 
/////////////////////File uploader
    $('#fileupload').on('submit', function(event){
        //event.stopPropagation();
        event.preventDefault();

        var sentNum = $('#sentNum').val();
        if(!sentNum || isNaN(sentNum)){
            sentNum = '5';
        }
        var data = new FormData();
        
        data.append('sentNum', sentNum);
        data.append('file', $('#file')[0].files[0]);
        // $.each(files, function(i, file){
        //      //console.log("file no: " + i + " file: " + file)
        //      data.append('file-' + (i+1), file);
        // });
        //data.append($('#file'[0]))

        for (var pair of data.entries()) {
            console.log(pair[0]+ ', ' + pair[1]); 
        }
        $.ajax({
            url: '/fileupload',
            type: 'POST',
            contentType: false,
            processData: false,
            dataType: 'json',
            data: data,         
            success: function(data){
                tinymce.get('highlighttext').setContent(data.og);
                var addText = '<ul>'
                for(i = 0; i<data.summary.length; i++){
                    addText = addText + '\n' + '<li onclick="highlight(this)">' + data.summary[i] + '</li>'
                }
                addText = addText + '</ul>'
                $('#textsummary_ifr').contents().find('#tinymce').append(addText);

            }
        })
    });


///////////////////////////Textbox
    var request;
    $('#textbox').on('submit', function(event){
        event.preventDefault();
        var sentNum = $('#sentNum').val()
        var text = $('#textarea').val()

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
                //data.og = original text, data.summary = array of summary points
                tinymce.get('highlighttext').setContent(data.og);

                //handle text highlighting here: when clicking the summary point, will highlight in original text

                var addText = '<ul>'
                for(i = 0; i<data.summary.length; i++){
                    addText = addText + '\n' + '<li onclick="highlight(this)">' + data.summary[i] + '</li>'
                    //$('#textsummary_ifr').contents().find('#tinymce').append('<li>' + data.summary[i] + '</li>');
                    //$('#textsummary').append('<li>' + data.summary[i] + '</li>')
                }
                addText = addText + '</ul>'
                $('#textsummary_ifr').contents().find('#tinymce').append(addText);
                
               
                return 'blah'
            },
            error: function(error){
                console.log("error for textbox")
            }
        });
        return 'blah'
    });


    /////////////////////////URL
    $('#externalurl').on('submit', function(e){
        e.preventDefault();
        var sentNum = $('#sentNum').val();
        var url = $('#url').val();
        //verify the url 

        fetch(url).then(res => res.blob()).then(blob => {
            let objectURL = URL.createObjectURL(blob);
            var data = new FormData();
            data.append('file', objectURL)
            $.ajax({

            });
        });


    });
        
    function afterSuccess(){
        console.log('successful file upload');
    }

            
    function beforeSubmit(){
        if (window.File && window.FileReader && window.FileList && window.Blob){
            if( !$('#file').val()) {
                $('#output').html('No file selected.');
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
                    $('#output').html('<b>'+ftype+'</b> Unsupported file type!');
                    return false
            }
        
            //Allowed file size is less than 50 MB (1MB: 1048576)
            if(fsize>52428800){
                $('#output').html('<b>'+bytesToSize(fsize) +'</b> Too big file! <br />File is too big, it should be less than 50 MB.');
                return false;
            }
                
            // $('#output').html('');  
        }
        else{
            //Output error to older unsupported browsers that doesn't support HTML5 File API
            $('#output').html('Please upgrade your browser, because your current browser lacks some new features we need!');
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
