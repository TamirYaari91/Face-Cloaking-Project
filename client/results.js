//region Imports

import {resizeImage} from "./shared_functions_and_consts.js";

//endregion

//region Constants

const resultsOriginalImageBox = document.getElementsByClassName("original_display_image")[0];
const resultsFaceOffImageBox = document.getElementsByClassName("faceoff_display_image")[0];
const resultsUlixesImageBox = document.getElementsByClassName("ulixes_display_image")[0];

const resultsJsonKeyToImageBoxClass = new Map();

const originalImageButton = document.getElementById("original_image_button");
const faceOffImageButton = document.getElementById("faceoff_image_button");
const ulixesImageButton = document.getElementById("ulixes_image_button");

const originalDSSIMTextBox = document.getElementById("original_dssim");
const faceOffDSSIMTextBox = document.getElementById("faceoff_dssim");
const ulixesDSSIMTextBox = document.getElementById("ulixes_dssim");

const originalEvasivenessMTextBox = document.getElementById("original_evasiveness");
const faceOffEvasivenessTextBox = document.getElementById("faceoff_evasiveness");
const ulixesEvasivenessTextBox = document.getElementById("ulixes_evasiveness");

const ulixesEvasivenessScoreMap = new Map([ // Calculated offline as explained in the report
    ["1", "59.24"],
    ["2", "74.62"],
    ["3", "83.12"],
    ["4", "92.1"],
    ["5", "93.52"]
])

//endregion

// region Functions
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

function openImageInNewTab(imageInputBase64) {
    fetch(imageInputBase64).then(res => res.blob())
        .then(blob => {
            const file = new File([blob], "File name", {type: "image/jpeg"})
            let link = URL.createObjectURL(file);
            window.open(link, "_blank");
        })
}

//endregion

resultsJsonKeyToImageBoxClass.set("original", resultsOriginalImageBox);
resultsJsonKeyToImageBoxClass.set("faceoff", resultsFaceOffImageBox);
resultsJsonKeyToImageBoxClass.set("ulixes", resultsUlixesImageBox);

let originalImageInputBase64 = "data:image/jpeg;base64," + localStorage.getItem("original_image");
let faceOffImageInputBase64 = "data:image/jpeg;base64," + localStorage.getItem("faceoff_image");
let ulixesImageInputBase64 = "data:image/jpeg;base64," + localStorage.getItem("ulixes_image");

let originalDSSIM = "<b>DSSIM:</b> " + "0"; // DSSIM between 2 identical images = 0
let faceOffDSSIM = "<b>DSSIM:</b> " + localStorage.getItem("faceoff_dssim");
let ulixesDSSIM = "<b>DSSIM:</b> " + localStorage.getItem("ulixes_dssim");

let rangeBarLevel = localStorage.getItem("range_bar_level");

let originalEvasivenessScore = "<b>Evasiveness Score:</b> " + "0"; // Original images will not fool VGGFace2
let ulixesEvasivenessScore = "<b>Evasiveness Score:</b> " + ulixesEvasivenessScoreMap.get(rangeBarLevel);

fillBoxWithImageFromJson(originalImageInputBase64, resultsOriginalImageBox);
fillBoxWithImageFromJson(faceOffImageInputBase64, resultsFaceOffImageBox);
fillBoxWithImageFromJson(ulixesImageInputBase64, resultsUlixesImageBox);

originalDSSIMTextBox.innerHTML = originalDSSIM;
faceOffDSSIMTextBox.innerHTML = faceOffDSSIM;
ulixesDSSIMTextBox.innerHTML = ulixesDSSIM;

originalEvasivenessMTextBox.innerHTML = originalEvasivenessScore;
ulixesEvasivenessTextBox.innerHTML = ulixesEvasivenessScore;


originalImageButton.onclick = function () {
    openImageInNewTab(originalImageInputBase64)
};
faceOffImageButton.onclick = function () {
    openImageInNewTab(faceOffImageInputBase64)
};
ulixesImageButton.onclick = function () {
    openImageInNewTab(ulixesImageInputBase64)
};

// localStorage.clear();
// TODO - Turn this ^ on after everything is done
