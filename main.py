import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Paths to the scripts
generate_script = Path(__file__).resolve().parent / 'scripts' / 'generate_clickstream_data.py'
upload_script = Path(__file__).resolve().parent / 'scripts' / 'upload_to_blob.py'

def run_script(script_path):
    result = subprocess.run(['python3', str(script_path)], capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)

if __name__ == "__main__":
    run_script(generate_script)
    run_script(upload_script)
