##############################################################################################
##                                                                                          ##
## This requirements.py file is related to The SearchMoon.py Excell Searching tool          ##
##                                                                                          ##
##        Author: Mahmut AY < mahmutayy@yahoo.com >                                         ##
##                                                                                          ##
##             USAGE: python3.x  requirements.py                                            ##  
##############################################################################################                                                                                       


import subprocess
import sys

def install(package):
    """
    Installs the given package using pip or pip3.
    """
    try:
        # Try using pip first
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except subprocess.CalledProcessError:
        try:
            # If pip fails, try using pip3
            subprocess.check_call([sys.executable, "-m", "pip3", "install", package])
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {package}. Error: {e}")

def check_and_install(package, import_name=None):
    """
    Checks if a package is installed. If not, it installs the package.
    """
    try:
        __import__(import_name or package)
        print(f"{package} is already installed.")
    except ImportError:
        print(f"{package} not found. Installing...")
        install(package)
        print(f"{package} has been installed successfully.")

if __name__ == "__main__":
    # List of required packages
    required_packages = {
        “pandas “ : “pandas “,
        “openpyxl “ : “openpyxl “,
        “xlrd” : “xlrd”        
         }

    # Let's Check and install each package
    for package, import_name in required_packages.items():
        check_and_install(package, import_name) 
      
