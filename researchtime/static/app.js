function compare() {
	
}

function startUpload(){
      document.getElementById('f1_upload_form').style.visibility = 'hidden';
      return true;
}

function stopUpload(success){
    var result = '';
    if (success == 1){
    	document.getElementById('result').innerHTML ='<span class="msg">Success<\/span><br/><br/>';
    }
    else{
        document.getElementById('result').innerHTML = '<span class="emsg">Error<\/span><br/><br/>';
    }
    return true;   
}