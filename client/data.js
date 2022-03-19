const uploadButton = document.getElementById("uploadButton");
const after = document.getElementById("after");
const allRanges = document.querySelectorAll(".range-wrap");
const prefRange = document.getElementById("prefRange");
const imageInput = document.querySelector("#image_input");
const image_box = document.getElementsByClassName("display_image")[0];
const MAX_SIZE_OF_IMAGE = 500; // square - will be true for both width and height


imageInput.addEventListener("change", function () {
    const reader = new FileReader();
    reader.addEventListener("load", () => {
        const uploaded_image = reader.result;
        image_box.style.backgroundImage = `url(${uploaded_image})`;
    });
    reader.readAsDataURL(this.files[0]);
    reader.onload = function (e) {
        const imageIn = new Image();
        imageIn.src = e.target.result;
        imageIn.onload = function () {
            let displaySize = resizeImage(this.width, this.height);
            image_box.style.width = displaySize[0] + "px";
            image_box.style.height = displaySize[1] + "px";
            return true;
        };
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

    // Get the receiver endpoint from Python using fetch:
    fetch("http://127.0.0.1:5000/params_receiver",
        {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'Accept': 'application/json'
            },

            // Strigify the payload into JSON:
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

const formData = new FormData();
formData.append('file', imageInput.files[0]);
const options = {
    method: 'POST',
    body: formData,
};

const uploadImageButton = document.getElementById("uploadImageButton");
uploadImageButton.onclick = function () {
    fetch("http://127.0.0.1:5000/image_receiver", options); // promise ignored - what comes back?
}

