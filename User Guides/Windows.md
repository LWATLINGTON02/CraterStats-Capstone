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

As of now, there are two methods for aquiring CraterstatsGUI on your local system
- Download the repository
  - ![image](https://github.com/user-attachments/assets/619683c5-c3d6-4bf9-87f8-a691013d97ab)


- If you have git installed you can `git clone` to your local machine.
```
git clone https://github.com/LWATLINGTON02/CraterStats-Capstone.git
```

After installing python, required dependencies, and downloading the application from github, navigate to the repository's directory within your system
Windows example:
```
cd CraterStats-Capstone
```

To run the application execute the following command
```
flet Alpha
```
With that the GUI should be running and ready to generate plots
