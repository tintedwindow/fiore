document.addEventListener("DOMContentLoaded", function() {
    
    // function to dynamically scale the image preview with the same ratio as calander day
    function updateAspectRatio() {
        var calDayDate = document.querySelector('.calendar-day-date');
        if (!calDayDate) return; // if the element isn't there, it returns simply.

        var calAspectRatio = calDayDate.clientWidth / calDayDate.clientHeight;
        var modalImageContainer = document.getElementById('modal-image-container');

        if (modalImageContainer) {
            modalImageContainer.style.aspectRatio = calAspectRatio.toString();
        }
    }

    // keep image file name short enough
    function shortenFilename(filename, maxLength = 30) {

        if (filename.length <= maxLength) {
            return filename;
        }

        let startChars = Math.ceil(maxLength  / 2) - 2;
        let endChars = Math.floor(maxLength / 2) - 1 - 1;
        
        return filename.substring(0, startChars) + '...' + filename.substring(filename.length - endChars);
    }
    // update aspect ratio initially
    updateAspectRatio();
    // update on resize
    window.addEventListener('resize', updateAspectRatio);


    var plusSigns = document.querySelectorAll('.calendar-day-date-add');
    var fileInput = document.getElementById('file-input');

    var modalImageDate = document.getElementById('modal-image-date');
    var modalDate = document.getElementById('modal-date');
    var monthYear = document.querySelector('.calendar-month-year');


    plusSigns.forEach(function(button) {
        button.addEventListener('click', function() {
            var dayDateNumber = this.closest('.calendar-day-date').querySelector('.calendar-day-date-number').textContent;
            modalImageDate.textContent = dayDateNumber;
            modalDate.textContent = dayDateNumber + monthYear.textContent;
            fileInput.click();
        });
    });


    // submission notification after clicking submit
    function showNotification(message, succesful, duration = 5000) {
        const notificationBar = document.getElementById('notification-bar');
        notificationBar.textContent = message; // Set text in it to be the status message
    
        // background color based on success
        if (succesful) {
            notificationBar.style.backgroundColor = '#B5C18E'; // Green for success
        } else {
            notificationBar.style.backgroundColor = '#FF8080'; // Red for error
        }
    
        notificationBar.style.display = 'flex'; 
    
        setTimeout(function() {
            notificationBar.style.display = 'none'; 
        }, duration);
    }

    var modal = document.getElementById('preview-modal');
    var modalImage = document.getElementById('modal-image');
    var modalText = document.getElementById('modal-text');


    fileInput.addEventListener('change', function () {
        if (this.files.length === 1) {
            var file = this.files[0];

            if (file.type.startsWith('image/')) {
                var fileURL = URL.createObjectURL(file);
                modalImage.src = fileURL;
                modalText.textContent = 'File selected: ' + shortenFilename(file.name);

                modal.style.display = "flex";
                document.getElementById('modal-input-text').focus();

                // revoking for saving ram or stuff. dbb said was good practice
                modalImage.onload = function() {
                    URL.revokeObjectURL(this.src);
                };
            } else {
                showNotification('Please select an image file (png, jpeg, jpg, jfif, gif, webp)', false, 5000);
                fileInput.value = ''; //resets file input
            }
        } else {
            alert('Please select exactly one image file.');
            fileInput.value = '';  // Reset file input
        }
    });

    // functioon to close the modal, reset some values
    function resetModal() {
        modalImage.src = '';
        fileInput.value = '';
        document.getElementById('modal-input-text').value = '';

        modal.style.display = "none";
    }


    // button clicking parts
    var modalSubmit = document.getElementById('modal-submit');
    var modalDiscard = document.getElementById('modal-discard');

    // close modal simply if discard is clicked
    modalDiscard.addEventListener('click', resetModal);

    
    // submission takes place here onwards

    // when I click the submit button
    modalSubmit.addEventListener('click', function() {

        // get current date number again :p
        var dayDateNumber = document.getElementById('modal-image-date').textContent;
        var image_description = document.getElementById('modal-input-text').value;
        var image_month = document.getElementById("file-month").value;
        var image_year = document.getElementById("file-year").value;

        if (fileInput.files.length > 0) {
            var dataToSend = new FormData();
            dataToSend.append('file', fileInput.files[0]);       
            dataToSend.append('date', dayDateNumber);
            dataToSend.append('month', image_month);
            dataToSend.append('year', image_year);
            dataToSend.append('description', image_description);

            fetch('/upload', {
                method: 'POST',
                body: dataToSend,
            })
            .then(response => {
                if (!response.ok) {  // Check if response is not OK (status not in the range 200-299)
                    return response.json().then(err => { throw new Error(err.error); })
                }
                return response.json();
            })
            .then(data => {
                console.log('Success:', data);

                // building an image element to place in
                let dayBox = document.getElementById('day-box-' + data.day);
                let img = document.createElement('img');
                img.src = data.filename;
                img.alt = "day-" + data.day;
                img.title = data.description ? data.description : '';
                img.className = "calendar-day-date-image";
                img.id = 'day-' + data.day;

                // building the outer anchor wrapper of the image element
                let imgWrapperLink = document.createElement('a');
                imgWrapperLink.href = "day-info?d=" + data.day + "&m=" + image_month + "&y=" + image_year;
                imgWrapperLink.style.width="100%";
                imgWrapperLink.style.height="100%";


                let dayBoxDate = document.querySelector('#day-box-' + data.day + ' div');
                dayBoxDate.classList.add("calendar-day-date-number-yes");

                let svgElement = document.querySelector('#day-box-' + data.day + ' svg');
                svgElement.parentNode.removeChild(svgElement);

                dayBox.appendChild(imgWrapperLink);
                imgWrapperLink.appendChild(img);

                resetModal();
                showNotification('File uploaded successfully!', true, 5000); // Show success message
            })
            .catch((error) => {
                console.error('Error:', error);
                resetModal();
                showNotification(error.message, false, 5000);  // http error stuff handling
            });        
        } else {
            resetModal();
            showNotification('Please select a file to upload', false, 5000);
        }
    });

        //handles if there is a redirect from delete i.e. a message

        var messageStatus= document.getElementById("message-status");

        if (messageStatus.textContent.trim() !== "") {
            showNotification(messageStatus.textContent.trim(), true, 5000);  
            messageStatus.textContent = "";
        }
});




