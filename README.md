<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/tn3w/TorWebsite/releases/download/imageupload/main_page.png">
  <source media="(prefers-color-scheme: light)" srcset="https://github.com/tn3w/TorWebsite/releases/download/imageupload/main_page_light.png">
  <img alt="Picture from Block Page" src="https://github.com/tn3w/TorWebsite/releases/download/imageupload/main_page.png">
</picture>
<a rel="noreferrer noopener" href="http://tn3wvjimrn3hydx4u52kzfnkgu6kffef2js27ewlhdf5htulno34vqad.onion"><img alt="Backup 1" src="https://img.shields.io/badge/Backup%201-141e24.svg?&style=for-the-badge&logo=torproject&logoColor=white"></a>  <p align="center"><a rel="noreferrer noopener" href="http://tn3wtor4vgnrimugptubpaqsf2gc4pcsktknkxt74w7p5yzbt7rwrkid.onion"><img alt="Backup 2" src="https://img.shields.io/badge/Backup%202-141e24.svg?&style=for-the-badge&logo=torproject&logoColor=white"></a>  <a rel="noreferrer noopener" href="http://tn3wtor7cfz3epmuetrhkj3mangjxqpd47lxxicfwwdwja6dwq6dbdad.onion"><img alt="Backup 3" src="https://img.shields.io/badge/Backup%203-141e24.svg?&style=for-the-badge&logo=torproject&logoColor=white"></a>

# TorWebsite
Source code of my Tor website.
If you want to use this code as your main page in conjunction with Tor or not, you can do so without attribution.

## 🚀 Installation
A. Use git
 1. Use the following command to download TorWebsite
    ```bash
    git clone https://github.com/tn3w/TorWebsite
    ```
 2. Go to the downloaded folder
    ```bash
    cd TorWebsite
    ```
 3. Install all required packages
    ```bash
    python3 -m pip install -r requirements.txt
    ```
    Or create a virtual environment with python3-venv and install the packages
    ```bash
    python3 -m venv .venv
    .venv/bin/python -m pip install -r requirements.txt
    ```
 4. Launch TorWebsite
    ```bash
    python3 main.py
    ```
    Or with a virtual environment:
    ```bash
    .venv/bin/python main.py
    ```

B. (Recommended for TOR users) Install via ZIP
 1. [Click here](https://github.com/tn3w/TorWebsite/archive/refs/heads/master.zip) to download the ZIP file as a normal user or [here](http://tn3wvjimrn3hydx4u52kzfnkgu6kffef2js27ewlhdf5htulno34vqad.onion/projects/TorWebsite?as_zip=1) [Mirror 1](http://tn3wtor4vgnrimugptubpaqsf2gc4pcsktknkxt74w7p5yzbt7rwrkid.onion/projects/TorWebsite?as_zip=1) [Mirror 2](http://tn3wtor7cfz3epmuetrhkj3mangjxqpd47lxxicfwwdwja6dwq6dbdad.onion/projects/TorWebsite?as_zip=1) as a Tor user
 2. Extract the downloaded ZIP packet with a packet manager or with the following command on Linux:
    ```bash
    unzip TorWebsite-master.zip -d TorWebsite
    ```
    Use the following if you downloaded it from the Tor Hidden Service:
    ```bash
    unzip TorWebsite.zip -d TorWebsite
    ```
 3. Go to the extracted folder
    ```bash
    cd TorWebsite
    ```
 4. Install all required packages
    ```bash
    python3 -m pip install -r requirements.txt
    ```
    Or create a virtual environment with python3-venv and install the packages
    ```bash
    python3 -m venv .venv
    .venv/bin/python -m pip install -r requirements.txt
    ```
 5. Launch CipherChat
    ```bash
    python3 main.py
    ```
    Or with a virtual environment:
    ```bash
    .venv/bin/python3 main.py
    ```