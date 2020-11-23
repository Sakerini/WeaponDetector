(function() {
    var video = document.getElementById('video'),
        vendorUrl = window.URL || window.webkitURL;

    navigator.getMedia = navigator.getUserMedia;
    
    // Capture
    navigator.getMedia({
        video: true,
        audio: false
    }, function(stream) {
        video.srcObject=stream
    }, function(error){
        // error
    });
}) ();