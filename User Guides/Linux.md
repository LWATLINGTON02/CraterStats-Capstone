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

### Error Handling

If receiving this error

```
error while loading shared libraries: libmpv.so.1: cannot open shared object file: No such file or directory
```

when trying to run

```
flet Alpha
```

Double check you have libmpv.so install by running

```
ldconfig -p | grep libmpv
```

If you have libmpv.so.2 and not libmpb.so.1 run this command with the path to libmpv.so.2 to create a symbolic link

For example:
```
sudo ln -s /usr/lib/x86_64-linux-gnu/libmpv.so.2 /usr/lib/x86_64-linux-gnu/libmpv.so.1
```
After running this command, run the application with
```
flet Alpha
```
and with that the GUI should be running and ready to generate plots
