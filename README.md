# dank_bank_v2
Group based interactive debt managing app

## Installation Instructions

### Submodule Usage
This project uses git submodules to clone it use these commands
```
git clone https://github.com/rhedgeco/dank_bank_v2.git
```
```
cd dank_bank_v2/
```
```
git submodule init
```
```
git submodule update
```

### Creating a Virtual Environment
you can run in your base python env, but when you install dependencies you may not want to install them to your
default python installation.

We will use virtualenvwrapper to handle our virtual environments.

For linux reference here. https://pypi.org/project/virtualenvwrapper/

For windows reference here. https://pypi.org/project/virtualenvwrapper-win/

To create a virtual environment:
```
mkvirtualenv dank_bank_v2_env
```
Any time you want to run the program you must be working inside the virtual environment:
```
workon dank_bank_v2_env
```
### Creating a virtual environment without virtualenvwrapper on Mac
First navigate to the dank bank directory in the terminal

Then create a virtual environment
```
virtualenv -p python3 venv
```
Then every time you want to use that environment to run the server, activate it
```
source venv/bin/activate
```
### Installing dependencies
dank_bank_v2 itself does not have any dependencies, but we depend on general_falcon_webserver, so we need to install
its dependencies. From inside the git repo folder run:
```
pip install -e general_falcon_webserver/.
```
Install dank_bank_v2's dependencies last
```
pip install -e .
```

### Run the app
To run the app, all we need to do is run:
```
python app.py
```