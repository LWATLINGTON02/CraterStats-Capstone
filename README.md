# CraterStats GUI

Northern Arizona University Senior Computer Science Capstone project.  
This project is to create a GUI for the current Craterstats CLI program.

## Installation

Due to the application still being in alpha stage, the initialization for execution has requirements.

We recommend installing a conda software package manager (anaconda or miniconda) to handle the python version and packages required for GUI usage.

You can download Anaconda [here](https://www.anaconda.com/download/success)

After instalation open the anaconda prompt and run the following commands:

Command for creating a new environment with python version 3.8
```
conda create -n craterstatsGUI python=3.8
```

Command for activating the newly created environment
```
conda activate craterstatsGUI
```

Install the required dependencies:

```
pip install flet
```
```
pip install craterstats
```

Download the ZIP file for the repository or `git clone` to your local machine.
```
git clone https://github.com/LWATLINGTON02/CraterStats-Capstone.git
```

After installing python, required dependencies, and downloading the application from github, navigate to the repository's directory within your system
Windows example:
```
cd Documents/Github/CraterStats-Capstone
```

To run the application execute the following command
```
flet run ./Alpha
```
With that the GUI should be executing and ready to generate plots

## Getting Started
Upon running the application you should be greeted with the home screen.

![image](https://github.com/user-attachments/assets/4ed48b5e-8ec8-4966-8f36-f16c8f153ff7)

In the toolbar, you can select the "Open" button from the "File" dropdown list. If you do not have your own plot configuration and data files, you can download samples here:
[Configuration File](https://github.com/LWATLINGTON02/CraterStats-Capstone/blob/main/Alpha/craterstats_config_files/checker.plt)
[Data File](https://github.com/LWATLINGTON02/CraterStats-Capstone/blob/main/Alpha/sample/sample.scc)

![image](https://github.com/user-attachments/assets/f7a10ca5-b683-4984-8cfd-8e31173a2881)

Select a plot configuration file.
![image](https://github.com/user-attachments/assets/a2d57c49-7c6f-4b94-a9ff-eb0dc209d537)

After uploading a configuration file select the Plot Settings tab
![image](https://github.com/user-attachments/assets/88d970e8-596e-408d-912f-ce9ae22fdc88)

Upon opening the Plot Settings page, upload a source file by selecting "Browse"
![image](https://github.com/user-attachments/assets/ce259393-73bf-4841-adb6-af27b59db951)

Select your source file
![image](https://github.com/user-attachments/assets/0fcbd837-fca0-4538-af53-72370c16d551)

After upload, the application should be displaying your plot configuration
![image](https://github.com/user-attachments/assets/6bd5898d-5fa6-4212-8baf-b4302821c56c)






## References

[Github](https://github.com/ggmichael/craterstats) of craterstats CLI program created and developed by Greg Michaels.
