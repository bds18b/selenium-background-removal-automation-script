# Background Removal Automation with Python Selenium

A Python script that automates background removal using an online Adobe tool.

## Table of Contents

- [Background Removal Automation with Python Selenium](#background-removal-automation-with-python-selenium)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Installation and Instructions](#installation-and-instructions)
  - [Issues / Bugs](#issues--bugs)
  - [Dependencies](#dependencies)
  - [License](#license)

## Introduction

This project provides a Python script that utilizes the Selenium library to automate background removal using an online Adobe tool. It simplifies the process of removing backgrounds from images by automating repetitive tasks and saving time. 


## Installation and Instructions

Clone the repository

To use this script, you need to have the Selenium library installed. You can install it using pip:

```bash
pip3 install selenium
```

You also need to install the WebDriver-Manager library for the webdriver to function:

```bash
pip3 install webdriver-manager
```

In order to run the script, you need to set up some credentials near the top of the script file. 
* adobe_email (your adobe email)                                                                    
* adobe_password (your adobe password)                                                      
* inbox_link (your tmail link)
  - If you don't have a tmail inbox, you can set one up here: https://tmail.link/
  - You then need to set up a forwarding protocol from your adobe email address that will forward the verification code emails to the tmail inbox. 
  - The script accesses the most recent email within the tmail inbox in order to retrieve the verification code. 


## Issues / Bugs

1. Script will crash if, when logging in, you are prompted to setup **2FA** or a **backup email**. All you need to do is click no and restart the script. These 2 cases typically occur consecutively and it is random.
   
2. After around 5 runs of the script, Adobe will lock your account for around 1 hour (if the runs are within a small time period). This is because Adobe counts these as failed login attempts for some reason. You will get an error that says "Your account has been locked due to multiple failed login attempts."


## Dependencies

- Python 3.8 or higher
- Selenium 3.141.0 or higher
- Webdriver Manager for Python


## License
[MIT License Text](https://opensource.org/licenses/MIT)
