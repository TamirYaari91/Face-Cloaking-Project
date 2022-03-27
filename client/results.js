const resultsPageHeader = document.getElementsByClassName("results_page_header");
const resultsGrayscaleImageBox = document.getElementsByClassName("grayscale_display_image")[0];
const resultsJsonKeyToImageBoxClass = new Map();
const MAX_SIZE_OF_IMAGE = 500; // square - will be true for both width and height
const grayscaleImageButton = document.getElementById("grayscale_image_button");
resultsJsonKeyToImageBoxClass.set("grayscale", resultsGrayscaleImageBox);

// shared code - need to figure out importing:
// func resize image
// const max size of image


// console.log(localStorage);


let grayscaleImageInputBase64 = localStorage.getItem("grayscale");
fillBoxWithImageFromJson(grayscaleImageInputBase64, resultsGrayscaleImageBox);
// This ^ will be replaced with a loop to fill all boxes


function fillBoxWithImageFromJson(imageInputBase64, imageBox) {
    imageInputBase64 = "data:image/jpeg;base64," + imageInputBase64;
    imageBox.style.backgroundImage = `url(${imageInputBase64})`;
    const imageIn = new Image();
    imageIn.src = imageInputBase64;
    imageIn.onload = function () {
        let displaySize = resizeImage(this.width, this.height);
        imageBox.style.width = displaySize[0] + "px";
        imageBox.style.height = displaySize[1] + "px";
        return true;
    }
}

function resizeImage(originalWidth, originalHeight) {
    let i = 1;
    let width = originalWidth;
    let height = originalHeight;
    while (width > MAX_SIZE_OF_IMAGE || height > MAX_SIZE_OF_IMAGE) {
        width = originalWidth / i;
        height = originalHeight / i;
        i = i + 0.5;
    }
    return [width, height];
}

grayscaleImageButton.onclick = function () {
    alert("button clicked")
    // optional:
    // send json to python, request file creation
    // python creates file on server, notifies js when done
    // js creates link and opens in a new tab
    // when are files deleted - perhaps after download? perhaps when session is over (how do I know?)
    // perhaps in the beginning of each session?
    // TBD...

}

// localStorage.clear(); TODO - Turn this on after everything is done
console.log(localStorage);
