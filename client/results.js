//region Imports

import {resizeImage} from "./shared_functions_and_consts.js";

//endregion

//region Constants

const resultsGrayscaleImageBox = document.getElementsByClassName("grayscale_display_image")[0];
const resultsFaceOffImageBox = document.getElementsByClassName("faceoff_display_image")[0];

const resultsJsonKeyToImageBoxClass = new Map();

const grayscaleImageButton = document.getElementById("grayscale_image_button");
const faceOffImageButton = document.getElementById("faceoff_image_button");


//endregion

resultsJsonKeyToImageBoxClass.set("grayscale", resultsGrayscaleImageBox);
resultsJsonKeyToImageBoxClass.set("faceoff", resultsFaceOffImageBox);

let grayscaleImageInputBase64 = "data:image/jpeg;base64," + localStorage.getItem("grayscale");
let faceOffImageInputBase64 = "data:image/jpeg;base64," + localStorage.getItem("faceoff");

fillBoxWithImageFromJson(grayscaleImageInputBase64, resultsGrayscaleImageBox);
fillBoxWithImageFromJson(faceOffImageInputBase64, resultsFaceOffImageBox);
// TODO - this ^ will be replaced with a loop to fill all boxes?


function fillBoxWithImageFromJson(imageInputBase64, imageBox) {
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

grayscaleImageButton.onclick = function () {
    fetch(grayscaleImageInputBase64)
        .then(res => res.blob())
        .then(blob => {
            const file = new File([blob], "File name",{ type: "image/jpeg" })
            let link = URL.createObjectURL(file);
            window.open(link, "_blank");
        })
}

faceOffImageButton.onclick = function () {
    fetch(faceOffImageInputBase64)
        .then(res => res.blob())
        .then(blob => {
            const file = new File([blob], "File name",{ type: "image/jpeg" })
            let link = URL.createObjectURL(file);
            window.open(link, "_blank");
        })
}

localStorage.clear();
// TODO - Turn this ^ on after everything is done
