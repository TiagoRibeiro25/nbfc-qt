import subprocess
from typing import List

def load_configs() -> List[str]:
    try:
        result = subprocess.run(
            ["nbfc", "config", "-l"], capture_output=True, text=True, check=True
        )
        return result.stdout.strip().splitlines()
    except subprocess.CalledProcessError as e:
        raise RuntimeError("Error executing 'nbfc config -l'") from e
