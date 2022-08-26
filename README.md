# FCP

FCP (Face Cloaking Project) is a Python-based framework for building and running a face obfuscation web platform.

## Installation

The project is written with Python 3.8 and was tested using this version. It is likely that any Python version from 3.6 and after will work as well, though different packages versions might be in need.

Use the package manager [pip](https://pip.pypa.io/en/stable/) or any other package manager to install the packages listed in the requirements.txt file.

## Usage

### Prerequisites

This is a pilot version, intended for the exclusive use of Tel Aviv University Computer Science department personnel only.

This is due to the fact that it uses TAU servers in order to run the Face-Off algorithm, for which a user & password are required (search for the TODO comments for the specific location where the credentials are to be entered).
In future versions, we will have the capacity to run Face-Off on our own servers, or a dedicated TAU user in order to do so.

In addition, you will need to be logged in to the TAU VPN, or to be connected to a TAU network.

In order to run the platform you will need to run the back end server and the web server simultaneously.

### Back End Server

* Open a terminal window
* Navigate to the server folder withing the FCP main folder
* Run the server.py file with python
```bash
cd /Users/.../FCP/server
python server.py
``` 
You should see the back end server running locally with the following address - http://127.0.0.1:5000/ 

### Web Server
* Open another terminal window
* Navigate to the client folder withing the FCP main folder
* Run an http.server with python
```bash
cd /Users/.../FCP/client
python -m http.server
```
You should see the web server running locally with the following address - http://localhost:8000/

### Using The Platform
* Open the website in a web browser using the mentioned address of the web server - http://localhost:8000/
* Use the "Choose file" button in order to browse for the face image you wish to cloak
* Set the privacy-usability parameter according to your preference
* Submit the image for cloaking using the "Upload image" button.

Once done, a new tab will be opened, containing the cloaked images as well as additional information (DSSIM, Evasiveness Score) about them.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
