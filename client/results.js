//region Imports

import {resizeImage} from "./shared_functions_and_consts.js";

//endregion

//region Constants

const resultsFaceOffImageBox = document.getElementsByClassName("faceoff_display_image")[0];
const resultsUlixesImageBox = document.getElementsByClassName("ulixes_display_image")[0];

const resultsJsonKeyToImageBoxClass = new Map();

const faceOffImageButton = document.getElementById("faceoff_image_button");
const ulixesImageButton = document.getElementById("ulixes_image_button");


//endregion

resultsJsonKeyToImageBoxClass.set("faceoff", resultsFaceOffImageBox);
resultsJsonKeyToImageBoxClass.set("ulixes", resultsUlixesImageBox);

let faceOffImageInputBase64 = "data:image/jpeg;base64," + localStorage.getItem("faceoff");
let ulixesImageInputBase64 = "data:image/jpeg;base64," + localStorage.getItem("ulixes");

fillBoxWithImageFromJson(faceOffImageInputBase64, resultsFaceOffImageBox);
fillBoxWithImageFromJson(ulixesImageInputBase64, resultsUlixesImageBox);

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

function displayImage(imageInputBase64) {
    fetch(imageInputBase64).then(res => res.blob())
        .then(blob => {
            const file = new File([blob], "File name", {type: "image/jpeg"})
            let link = URL.createObjectURL(file);
            window.open(link, "_blank");
        })
}

faceOffImageButton.onclick = function () {
    displayImage(faceOffImageInputBase64)
};
ulixesImageButton.onclick = function () {
    displayImage(ulixesImageInputBase64)
}

// localStorage.clear();
// TODO - Turn this ^ on after everything is done
