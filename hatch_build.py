import os
import sys
import shutil
import subprocess
import urllib.request
import tempfile
from pathlib import Path
from hatchling.builders.hooks.plugin.interface import BuildHookInterface

class CustomBuildHook(BuildHookInterface):
    def initialize(self, version, build_data):
        """
        This is called during the build process.
        We trigger the parser generation here.
        """
        self.generate_parser()

    def generate_parser(self):
        root = Path(self.root)
        grammar_file = root / "grammar" / "Varphi.g4"
        output_dir = root / "src" / "varphi_devkit" / "parser"
        antlr_url = "https://www.antlr.org/download/antlr-4.13.2-complete.jar"

        if not shutil.which("java"):
            sys.exit("Error: 'java' executable not found in PATH. Java is required to build the parser.")

        print("Generating ANTLR parser...", file=sys.stderr)
        
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "__init__.py").touch()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".jar") as tmp_jar:
            try:
                with urllib.request.urlopen(antlr_url) as response:
                    shutil.copyfileobj(response, tmp_jar)
                tmp_jar.close()

                cmd = [
                    "java", "-jar", tmp_jar.name,
                    "-Dlanguage=Python3",
                    "-o", str(output_dir),
                ]
                
                subprocess.run(cmd, check=True)
                print(f"Success. Parser generated in {output_dir}", file=sys.stderr)

            except subprocess.CalledProcessError as e:
                sys.exit(f"Error during ANTLR generation: {e}")
            finally:
                if os.path.exists(tmp_jar.name):
                    os.remove(tmp_jar.name)