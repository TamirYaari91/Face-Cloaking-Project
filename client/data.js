// let pageId = document.head.id;
// let isUploadPage = pageId === "upload_page"
// let isResultsPage = pageId === "results_page"

const MAX_SIZE_OF_IMAGE = 500; // square - will be true for both width and height
const uploadButton = document.getElementById("uploadButton");
const after = document.getElementById("after");
const allRanges = document.querySelectorAll(".range-wrap");
const prefRange = document.getElementById("prefRange");
const uploadImageInput = document.querySelector("#image_input");
const uploadImageBox = document.getElementsByClassName("display_image")[0];
const uploadImageButton = document.getElementById("uploadImageButton");
let uploadImageInputBase64;
let isCloakingCompleted = Boolean(0);

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

uploadButton.onclick = function () {
    let inputs_json = [
        {"prefValue": parseInt(prefRange.value)}
    ];

    fetch("http://127.0.0.1:5000/params_receiver",
        {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'Accept': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            body: JSON.stringify(inputs_json)
        }).then(res => {
        if (res.ok) {
            return res.json()
        } else {
            alert("something is wrong") // needs to be clarified
        }
    }).then(jsonResponse => {
            let json = jsonResponse[0];
            after.innerHTML += "Returned from Python (should be range value +1):" + "<p>";
            after.innerHTML += "prefValue = " + json.prefValue + "<p>";
        }
    ).catch((err) => console.error(err));
}

uploadImageButton.onclick = function () {
    let image_json = [
        {"imageData": uploadImageInputBase64}
    ];

    fetch("http://127.0.0.1:5000/image_receiver", {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify(image_json)
    }).then(res => {
        if (res.ok) {
            return res.json()
        } else {
            alert("something is wrong") // needs to be clarified
        }
    })
        .then(jsonResponse => {
            // check if cloaking was made - nothing came back empty or something like that

            isCloakingCompleted = Boolean(1);

            for (let key in jsonResponse) {
                if (key === "success") {
                    continue;
                }
                let value = jsonResponse[key];
                localStorage.setItem(key, value);
            }
            console.log(localStorage);
        })
        .catch((err) => console.error(err));
}

