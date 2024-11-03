import json
import subprocess
from typing import Optional

def is_nbfc_installed() -> bool:
    try:
        subprocess.run(["nbfc", "--help"], check=True, stdout=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

def get_pc_model() -> str:
    try:
        result = subprocess.run(
            ["nbfc", "get-model-name"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return "Unknown model"

def get_current_config() -> Optional[str]:
    try:
        result = subprocess.run(
            ["cat", "/etc/nbfc/nbfc.json"],
            capture_output=True,
            text=True,
            check=True
        )
        data = json.loads(result.stdout)
        return data.get("SelectedConfigId", "")
    except subprocess.CalledProcessError as e:
        if "No such file or directory" in e.stderr:
            return None
        else:
            raise  # re-raise any other exceptions

def apply_nbfc_config(config_name: str) -> None:
    try:
        command = ["pkexec", "nbfc", "config", "--set", config_name]
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to apply config: {e}")


def get_nbfc_status() -> str:
    """ Returns the status of nbfc service (running or stopped) """
    try:
        result = subprocess.run(
            ["nbfc", "status"],
            capture_output=True,
            text=True,
            check=True
        )
        output: str = result.stdout.strip()

        if "Read-only" in output:
            return "running"
        else:
            return "stopped"

    except:
        return "stopped"

def start_nbfc() -> None:
    try:
        command = ["pkexec", "nbfc", "start"]
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to start nbfc: {e}")

def stop_nbfc() -> None:
    try:
        command = ["pkexec", "nbfc", "stop"]
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to stop nbfc: {e}")

def restart_nbfc() -> None:
    try:
        command = ["pkexec", "nbfc", "restart"]
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to restart nbfc: {e}")
