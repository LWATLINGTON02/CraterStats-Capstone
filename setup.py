from setuptools import setup, find_packages

setup(
    name="Alpha",                    # Project name
    version="1.0.0",                      # Version
    author="Lunar Pit Patrol",
    author_email="EPalmisanoConnect@gmail.com",
    description="A graphical user interface for improving user experience when computing and generating crater statistics.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/LWATLINGTON02/CraterStats-Capstone/tree/main",  # Project's GitHub URL
    packages=find_packages(),             # Automatically find and include packages
    include_package_data=True,            # Include additional files specified in MANIFEST.in
    install_requires=[
        "flet",                           # Dependencies for your project
        "craterstats"
    ],
    classifiers=[                         # Optional, for better categorization on PyPI
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "craterstats-gui=Alpha.run_alpha:main",  # This makes 'my_project' a command-line command
        ],
    },
    python_requires=">=3.8.0",              # Minimum Python version
)
