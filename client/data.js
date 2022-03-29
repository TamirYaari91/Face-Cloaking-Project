//region Imports

import {resizeImage} from "./shared_functions_and_consts.js";

//endregion

//region Constants

const after = document.getElementById("after");
const allRanges = document.querySelectorAll(".range-wrap");
const prefRange = document.getElementById("prefRange");
const uploadImageInput = document.querySelector("#image_input");
const uploadImageBox = document.getElementsByClassName("display_image")[0];
const uploadImageButton = document.getElementById("uploadImageButton");
const jsonHeaders = {
    'Content-type': 'application/json',
    'Accept': 'application/json'}
const domain = "http://127.0.0.1:5000/";

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
});

// export function resizeImage(originalWidth, originalHeight) {
//     let i = 1;
//     let width = originalWidth;
//     let height = originalHeight;
//     while (width > MAX_SIZE_OF_IMAGE || height > MAX_SIZE_OF_IMAGE) {
//         width = originalWidth / i;
//         height = originalHeight / i;
//         i = i + 0.5;
//     }
//     return [width, height];
// }

allRanges.forEach(wrap => {
    const range = wrap.querySelector(".range");
    const bubble = wrap.querySelector(".bubble");
    range.addEventListener("input", () => {
        setBubble(range, bubble);
    });
    setBubble(range, bubble);
});

function setBubble(range, bubble) {
    const val = range.value;
    const min = range.min ? range.min : 0;
    const max = range.max ? range.max : 100;
    const newVal = Number(((val - min) * 100) / (max - min));
    bubble.innerHTML = val;

    // Sorta magic numbers based on size of the native UI thumb
    bubble.style.left = `calc(${newVal}% + (${8 - newVal * 0.15}px))`;
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

async function extractPrefValueFromJsonUpdateHTML(json) {
    json = json[0];
    after.innerHTML += "Returned from Python (should be range value +1):" + "<p>";
    after.innerHTML += "prefValue = " + json.prefValue + "<p>";
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

async function uploadImageClick() {
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
}

uploadImageButton.onclick = async function () {
    let ignore = uploadImageClick();

    await new Promise(r => setTimeout(r, 200));
    //TODO ^
    // Instead of this, will need to wait for a type of signal from the server
    // that cloaking is completed before loading results page

    window.open("results.html", "_blank");
}

