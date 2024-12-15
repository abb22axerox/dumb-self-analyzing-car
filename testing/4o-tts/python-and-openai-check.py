import sys
import importlib.util
import os

def print_python_info():
    # Print Python version
    print("Python Version:")
    print(sys.version)
    print("")

    # Print Python Install Directory
    print("Python Install Directory:")
    print(sys.prefix)
    print("")

    # Print the PATH environment variable
    print("PATH Environment Variable:")
    print(os.getenv("PATH"))
    print("")

    # Print PYTHONPATH if it's set
    print("PYTHONPATH Environment Variable:")
    pythonpath = os.getenv("PYTHONPATH")
    if pythonpath:
        print(pythonpath)
    else:
        print("Not Set")
    print("")

    # Print PYTHONHOME if it's set
    print("PYTHONHOME Environment Variable:")
    pythonhome = os.getenv("PYTHONHOME")
    if pythonhome:
        print(pythonhome)
    else:
        print("Not Set")
    print("")

    # Attempt to import the 'openai' module and print its version and file location
    try:
        # Importing the openai module
        import openai
        
        # Print openai module version if available
        print("OpenAI Module Version:")
        if hasattr(openai, '__version__'):
            print(openai.__version__)
        else:
            print("Version not specified")
        print("")

        # Print location of the openai module
        print("OpenAI Module Location:")
        print(importlib.util.find_spec("openai").origin)
        print("")
    
    except ImportError:
        print("OpenAI module is not installed")
        print("")

if __name__ == "__main__":
    print_python_info()