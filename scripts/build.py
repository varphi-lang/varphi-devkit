import subprocess
import sys
import shutil
import urllib.request
import tempfile
import os
from pathlib import Path

# Configuration
ANTLR_DOWNLOAD_URL = "https://www.antlr.org/download/antlr-4.13.2-complete.jar"

# Paths
ROOT = Path(__file__).parent.parent
GRAMMAR_FILE = ROOT / "grammar" / "Varphi.g4"
# Using the path from your snippet:
OUTPUT_DIR = ROOT / "src" / "varphi_devkit" / "parser"

def check_java_installed():
    if not shutil.which("java"):
        print("Error: 'java' executable not found in PATH.")
        print("Please install Java and ensure it is added to your environment variables.")
        sys.exit(1)

def generate_parser():
    check_java_installed()

    if not GRAMMAR_FILE.exists():
        print(f"Error: Grammar file not found at {GRAMMAR_FILE}")
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "__init__.py").touch()

    print(f"Downloading ANTLR jar to tempfile...")
    
    # Create a temp file. delete=False is required for Windows compatibility
    # so we can close the file before Java tries to open it.
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jar") as tmp_jar:
        try:
            # 1. Download
            with urllib.request.urlopen(ANTLR_DOWNLOAD_URL) as response:
                shutil.copyfileobj(response, tmp_jar)
            
            # Close the file handle so Java can read it
            tmp_jar.close()

            # 2. Run Java
            cmd = [
                "java",
                "-jar", tmp_jar.name,
                "-Dlanguage=Python3",
                "-o", str(OUTPUT_DIR),
                str(GRAMMAR_FILE)
            ]
            
            print(f"Generating parser...")
            subprocess.run(cmd, check=True)
            print("Success. Parser generated in src/varphi_devkit/parser/")

        except subprocess.CalledProcessError as e:
            print("Error during ANTLR generation.")
            sys.exit(e.returncode)
        finally:
            # 3. Cleanup: Delete the temp file manually
            if os.path.exists(tmp_jar.name):
                os.remove(tmp_jar.name)

if __name__ == "__main__":
    generate_parser()