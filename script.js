document.addEventListener('DOMContentLoaded', () => {
    const imageUploadInput = document.getElementById('imageUpload');
    const countButton = document.getElementById('countButton');
    const peopleCount = document.getElementById('peopleCount');

    countButton.addEventListener('click', () => {
        if (imageUploadInput.files.length === 0) {
            alert('Please select an image.');
            return;
        }

        const formData = new FormData();
        formData.append('image', imageUploadInput.files[0]);

        fetch('http://localhost:5000/count_people', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                console.log(data); // Log the received data to the console for debugging

                if (data.error) {
                    alert('Error: ' + data.error);
                } else {
                    const countElement = document.getElementById('peopleCount');
                    countElement.textContent = 'People Count: ' + data.people_count;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred. Please check the browser console for more details.');
            });
    });
});
