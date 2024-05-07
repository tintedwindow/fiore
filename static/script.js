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

                // revoking for saving ram or stuff. dbb said was good practice
                modalImage.onload = function() {
                    URL.revokeObjectURL(this.src);
                };
            } else {
                alert('Please select an image file (jpeg or png)!');
                fileInput.value = ''; //resets file input
            }
        } else {
            alert('Please select exactly one image file.');
            fileInput.value = '';  // Reset file input
        }
    });

    var modalSubmit = document.getElementById('modal-submit');
    var modalDiscard = document.getElementById('modal-discard');

    function resetModal() {
        modalImage.src = '';
        fileInput.value = '';
        modal.style.display = "none";
    }

    modalSubmit.addEventListener('click', resetModal);
    modalDiscard.addEventListener('click', resetModal);
});