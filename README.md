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

## References

[Github](https://github.com/ggmichael/craterstats) of craterstats CLI program created and developed by Greg Michaels.
