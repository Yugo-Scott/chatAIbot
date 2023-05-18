// static/js/upload-audio.js
document.getElementById('recorder-button').addEventListener('click', function() {
  document.getElementById('audio-file').click();
});

document.getElementById('audio-file').addEventListener('change', function() {
  var file = this.files[0];
  if (file) {
    var formData = new FormData();
    formData.append('file', file);
    fetch('/post-audio-get/', {
      method: 'POST',
      body: formData
    })
    .then(response=>response.blob())
    .then(blob=>{
      const audioElement = document.createElement('audio');
      audioElement.src = URL.createObjectURL(blob);
      audioElement.controls = true;
      document.querySelector('.audio-putput').appendChild(audioElement);
    })
    // .then(function(response) {
    //   if (response.ok) {
    //     // response.then(function(data) {
    //       console.log(response);
    //       // Create a link to download the generated audio
    //       var link = document.createElement('audio');
    //       link.href = '/audio/output.mp3'; // Change this to '/audio/' + data.filename if server returns filename
    //       link.download = 'Download the generated audio';
    //       link.innerText = 'Download the generated audio';

    //       // Append the link to the container
    //       document.querySelector('.audio-putput').appendChild(link);
    //     // });
    //     console.log('Audio file was uploaded successfully');
    //   } else {
    //     console.error('Audio file upload failed');
    //   }
    // });
  }
});

