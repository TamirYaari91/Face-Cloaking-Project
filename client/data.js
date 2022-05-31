//region Imports

import {resizeImage} from "./shared_functions_and_consts.js";

//endregion

//region Constants

const prefRange = document.getElementById("prefRange");
const loadingMessage = document.getElementById("loadingMessage");
const spinner = document.getElementById("spinner");
const uploadImageInput = document.querySelector("#image_input");
const uploadImageBox = document.getElementsByClassName("display_image")[0];
const uploadImageButton = document.getElementById("uploadImageButton");
const jsonHeaders = {
    'Content-type': 'application/json',
    'Accept': 'application/json'
}
const domain = "http://127.0.0.1:5000/";
let isFileChosen = false;

//endregion

let uploadImageInputBase64;

localStorage.clear();

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

async function postJsonToPythonAPI(domain, subdirectory, jsonBody) {
    const fullPath = domain + subdirectory;
    const fullJson = {
        method: 'POST',
        headers: jsonHeaders,
        body: JSON.stringify(jsonBody)
    };
    return fetch(fullPath, fullJson);
}

async function extractPrefValueFromJsonUpdateHTML(json) {
    json = json[0];
    console.log("Returned from Python = range+1");
    console.log("prefValue = " + json.prefValue)
    // after.innerHTML +=  + "<p>";
}

async function extractJsonFromFetchRes(res) {
    if (res.ok) {
        return res.json();
    } else {
        alert("something is wrong");
    }
}

async function extractImageFromJsonAddToLocalStorage(json) {
    for (let key in json) {
        if (key === "success") {
            continue;
        }
        let value = json[key];
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
        {"prefValue": parseInt(prefRange.value)}];

    let fetchRes = await postJsonToPythonAPI(domain, "params_receiver", jsonBody);
    let jsonFromFetchRes = await extractJsonFromFetchRes(fetchRes);
    await extractPrefValueFromJsonUpdateHTML(jsonFromFetchRes);

    jsonBody = [
        {"imageData": uploadImageInputBase64}];

    fetchRes = await postJsonToPythonAPI(domain, "image_receiver", jsonBody);
    jsonFromFetchRes = await extractJsonFromFetchRes(fetchRes);
    await extractImageFromJsonAddToLocalStorage(jsonFromFetchRes);
    return true;
}

uploadImageButton.onclick = async function () {
    let isFileUploaded = await uploadImageClick();
    if (isFileUploaded) {
        window.open("results.html", "_blank"); //TODO - change to _self
    }
    loadingMessage.style.display = "none";
    spinner.style.display = "none";
}

