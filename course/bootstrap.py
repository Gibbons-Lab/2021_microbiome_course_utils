"""Bootstrap some dependencies on Colab."""

import os
import shutil
from .utils import download, con

prodigal_url = (
    "https://github.com/hyattpd/Prodigal/releases/download/v2.6.3/prodigal.linux"
)


def am_i_colab():
    """Check if running on colab."""
    state = (
        os.path.exists("/content")
        and os.environ.get("HOME") == "/root"
        and "DATALAB_SETTINGS_OVERRIDES" in os.environ
        and "COLAB_GPU" in os.environ
    )
    return state


def main():
    """Install some dependencies."""
    if am_i_colab():
        download(prodigal_url, "/usr/local/bin/prodigal")
        os.chmod("/usr/local/bin/prodigal", 755)
        con.log(":hammer: Set up [green]prodigal[/green].")
        if os.path.exists("/content/sample_data"):
            shutil.rmtree("/content/sample_data")
        con.log(":hammer: All clean now.")
    else:
        con.print(
            ":fearful: This does not look like Colab, I better not touch anything."
        )
