import subprocess

def install_dependencies():
    try:
        subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
        print("Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install dependencies: {e}")

if __name__ == "__main__":
    install_dependencies()
