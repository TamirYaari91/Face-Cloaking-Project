import {resizeImage} from "./shared_functions_and_consts.js";

//region Constants
const prefRange = document.getElementById("prefRange");
const loadingMessage = document.getElementById("loadingMessage");
const spinner = document.getElementById("spinner");
const uploadImageInput = document.querySelector("#image_input");
const uploadImageBox = document.getElementsByClassName("display_image")[0];
const uploadImageButton = document.getElementById("uploadImageButton");
const ulixesToggleButton = document.getElementById("ulixes_toggle");
const faceOffToggleButton = document.getElementById("faceoff_toggle");
const jsonHeaders = {
    'Content-type': 'application/json',
    'Accept': 'application/json'
}
const domain = "http://127.0.0.1:5000/";
//endregion

//region Variables

let isFileChosen = false;
let uploadImageInputBase64;
let runUlixes = true;
let runFaceOff = true;
let errorOccurred = false;
//end region

// region Functions
function fillBoxWithImageFromFile(e, imageBox) {
    const imageIn = new Image();
    imageIn.src = e.target.result;
    imageIn.onload = function () {
        let displaySize = resizeImage(this.width, this.height);
        imageBox.style.width = displaySize[0] + "px";
        imageBox.style.height = displaySize[1] + "px";
        imageBox.style.border = "1px solid black";
        return true;
    }
}

async function postJsonToPythonAPI(domain, subdirectory, jsonBody) {
    const fullPath = domain + subdirectory;
    const fullJson = {
        method: 'POST',
        headers: jsonHeaders,
        body: JSON.stringify(jsonBody)
    };
    return fetch(fullPath, fullJson);
}

async function extractJsonFromFetchRes(res) {
    if (res.ok) {
        return res.json();
    } else {
        alert("something is wrong");
    }
}

async function extractDataFromJsonAddToLocalStorage(json) {
    for (let key in json) {
        let value = json[key];
        if (key === "success") {
            if (value === false) {
                errorOccurred = true;
                let errorMessage = "";
                let faceOffError = localStorage.getItem("error_faceoff");
                let ulixesError = localStorage.getItem("error_ulixes");
                if (faceOffError != null) {
                    errorMessage += "An error has occurred in Face-Off: " + faceOffError + "\n";
                }
                if (ulixesError != null) {
                    errorMessage += "An error has occurred in Ulixes: " + ulixesError + "\n";
                }
                alert(errorMessage);
            }
        }
        localStorage.setItem(key, value);
    }
}

function updateLoadingSection(isFileChosen) {
    loadingMessage.style.display = "block";
    if (isFileChosen === false) {
        loadingMessage.innerHTML = "You did not choose a file.";
        loadingMessage.style.color = "red";
        return false;
    }
    loadingMessage.innerHTML = "Cloaking...";
    loadingMessage.style.color = "black";
    spinner.style.display = "inline-block";
    return true;
}

async function uploadImageClick() {
    updateLoadingSection(isFileChosen);
    if (isFileChosen === false) {
        return false;
    }

    let jsonBody = [
        {
            "prefValue": parseInt(prefRange.value),
            "runUlixes": runUlixes,
            "runFaceOff": runFaceOff
        }];
    await postJsonToPythonAPI(domain, "params_receiver", jsonBody);
    jsonBody = [{"imageData": uploadImageInputBase64}];

    let fetchRes = await postJsonToPythonAPI(domain, "image_receiver", jsonBody);
    let jsonFromFetchRes = await extractJsonFromFetchRes(fetchRes);
    await extractDataFromJsonAddToLocalStorage(jsonFromFetchRes);
    return true;
}
// endregion

localStorage.clear();

ulixesToggleButton.onclick = function () {
    runUlixes = !runUlixes;
}

faceOffToggleButton.onclick = function () {
    runFaceOff = !runFaceOff;
}


uploadImageInput.addEventListener("change", function () {
    const reader = new FileReader();
    reader.addEventListener("load", () => {
        uploadImageInputBase64 = reader.result;
        uploadImageBox.style.backgroundImage = `url(${uploadImageInputBase64})`;
    });
    reader.readAsDataURL(this.files[0]);
    reader.onload = function (e) {
        fillBoxWithImageFromFile(e, uploadImageBox);
    };
    isFileChosen = true;
});

uploadImageButton.onclick = async function () {
    let isFileUploaded = await uploadImageClick();
    if (isFileUploaded && !errorOccurred) {
        window.open("results.html", "_blank");
    }
    loadingMessage.style.display = "none";
    spinner.style.display = "none";
}

