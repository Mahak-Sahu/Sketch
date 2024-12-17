function clearOldSketch() {
    // Clear the existing sketch image and hide the result section
    const sketchImage = document.getElementById('sketchImage');
    sketchImage.src = '';
    sketchImage.alt = 'Sketch will appear here';
    document.getElementById('result').style.display = 'none';
}

function uploadImage() {
    const fileInput = document.getElementById('imageInput');
    const file = fileInput.files[0];
    
    if (!file) {
        alert("Please select an image file first.");
        return;
    }

    const formData = new FormData();
    formData.append('image', file);

    fetch('/convert', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const sketchImage = document.getElementById('sketchImage');
            sketchImage.src = data.sketch_url + '?' + new Date().getTime();
            sketchImage.alt = 'Sketch Image';
            document.getElementById('result').style.display = 'block';
        } else {
            alert("Failed to convert the image.");
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
