// Get the button and container from HTML:
const button = document.getElementById("theButton")
const before = document.getElementById("before")
const after = document.getElementById("after")

// make x and y as input from user

// insert all the logic that happens after submit to the submit function - using additional functions
// need to check how it is done without just disappearing immediately :(


// const form = document.getElementById("form");
// const log = document.getElementById("log");
const submit = document.getElementById("submit");

function logSubmit(event) {
    x = document.getElementById("x").value;
    y = document.getElementById("y").value;
    // x = x_inp;
    // y = y_inp;
    before.innerHTML += "Sending to Python:" + "<p>" +
        "x = " + x + "<p>" + "y = " + y + "<p>";
    // event.preventDefault();
    console.log("in first button click func : x = "+x);
}

// form.addEventListener('submit',logSubmit);

submit.addEventListener('click',logSubmit);

let x = 1; // this can be the picture
let y = 3; // this can be the level of privacy-usability or whatever

console.log("out of func : x = "+x);

// submit.onclick = function () {
//     let x_inp = document.getElementById("x").value;
//     let y_inp = document.getElementById("y").value;
//     // log.textContent = x_inp + "<pr>" + y_inp;
//     log.innerHTML = x_inp + "<br>" + y_inp;
//     x = x_inp;
//     y = y_inp;
//     before.innerHTML += "Sending to Python:" + "<p>" +
//         "x = " + x + "<p>" + "y = " + y + "<p>";
// }

let inputs = [x, y];
// let inputs_json = [
//     {"x": x, "y": y}
// ];

// before.innerHTML += "Sending to Python:" + "<p>" +
//     "x = " + x + "<p>" + "y = " + y + "<p>";

// Create an event listener on the button element:
button.onclick = function () {
    let inputs_json = [
        {"x": parseInt(x), "y": parseInt(y)}
    ];

    console.log("in post to python func : x = "+x);


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
