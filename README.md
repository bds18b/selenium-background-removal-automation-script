# Background Removal Automation with Python Selenium

A Python script that automates background removal using an online Adobe tool.

## Table of Contents

- [Background Removal Automation with Python Selenium](#background-removal-automation-with-python-selenium)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Installation](#installation)
  - [Issues / Bugs](#issues--bugs)

## Introduction

This project provides a Python script that utilizes the Selenium library to automate background removal using an online Adobe tool. It simplifies the process of removing backgrounds from images by automating repetitive tasks and saving time. 


## Installation

To use this script, you need to have the Selenium library installed. You can install it using pip:

```bash
pip install selenium
```

## Issues / Bugs

1. Script will crash if, when logging in, you are prompted to setup **2FA** or a **backup email**. All you need to do is click no and restart the script. These 2 cases typically occur consecutively and it is random.
   
2. After around 5 runs of the script, Adobe will lock your account for around 1 hour (if the runs are within a small time period). This is because Adobe counts these as failed login attempts for some reason. You will get an error that says "Your account has been locked due to multiple failed login attempts."
