import os
import subprocess
import sys

def install_pyinstaller():
    """Check if PyInstaller is installed; install if not."""
    try:
        __import__("PyInstaller")
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def build_executable(app_folder, main_script):
    """
    Build the Flask app into an executable.

    Parameters:
        app_folder (str): The folder containing the Flask app files.
        main_script (str): The main Python file of the Flask app (e.g., "app.py").
    """
    # Define paths
    templates_path = os.path.join(app_folder, "templates")
    static_path = os.path.join(app_folder, "static")
    
    # Verify paths
    if not os.path.isfile(os.path.join(app_folder, main_script)):
        raise FileNotFoundError(f"{main_script} not found in {app_folder}")
    
    if not os.path.isdir(templates_path) or not os.path.isdir(static_path):
        raise FileNotFoundError("templates or static folder not found in the specified app folder.")
    
    # Set up the PyInstaller command
    command = [
        "pyinstaller",
        "--onefile",
        f"--name={os.path.basename(app_folder)}",  # Name of the executable
        f"--add-data={templates_path}:templates",
        f"--add-data={static_path}:static",
        os.path.join(app_folder, main_script)
    ]
    
    print("Building the executable with PyInstaller...")
    subprocess.run(command, check=True)
    print("\nBuild complete. The executable is located in the 'dist' folder.")

def main():
    # Define your Flask app folder and main script file
    app_folder = input("Enter the path to your Flask app folder: ").strip()
    #app_folder = "C:\Users\suhas\Downloads\my_flash_app"
    main_script = input("Enter the main script filename (e.g., 'app.py'): ").strip()
    
    # Install PyInstaller if needed
    install_pyinstaller()
    
    # Run the build process
    try:
        build_executable(app_folder, main_script)
    except Exception as e:
        print(f"Error during build: {e}")

if __name__ == "__main__":
    main()
