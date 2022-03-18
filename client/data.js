const postToPython = document.getElementById("postToPython")
const before = document.getElementById("before")
const after = document.getElementById("after")
const inputSubmit = document.getElementById("inputSubmit");
const allRanges = document.querySelectorAll(".range-wrap");
const prefRange = document.getElementById("prefRange");

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


inputSubmit.addEventListener('click',function () {
    x = document.getElementById("x").value;
    y = prefRange.value;
    before.innerHTML += "Sending to Python:" + "<p>" +
        "x = " + x + "<p>" + "Value from range: = " + y + "<p>";
});

let x; // this can be the picture
let y; // this can be the level of privacy-usability or whatever

postToPython.onclick = function () {
    let inputs_json = [
        {"x": parseInt(x), "y": parseInt(y)}
    ];

    // Get the receiver endpoint from Python using fetch:
    fetch("http://127.0.0.1:5000/receiver",
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
            alert("something is wrong")
        }
    }).then(jsonResponse => {
            let json = jsonResponse[0];
            after.innerHTML += "Returned from Python:" + "<p>";
            after.innerHTML += "x = " + json.x + "<p>";
            after.innerHTML += "y = " + json.y + "<p>";
        }
    ).catch((err) => console.error(err));
}
