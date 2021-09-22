"""Bootstrap some dependencies on Colab."""

import os
from .utils import download, con

prodigal_url = (
    "https://github.com/hyattpd/Prodigal/"
    "releases/download/v2.6.3/prodigal.linux"
)


def am_i_colab():
    """Check if running on colab."""
    state = (
        os.path.exists("/content") and
        os.environ.get("HOME") == "root" and
        "DATALAB_SETTINGS_OVERRIDES" in os.environ and
        os.environ.get("GCE_METADATA_TIMEOUT") == "0"
    )
    return state


def main():
    """Install some dependencies."""
    if am_i_colab():
        download(prodigal_url, "/usr/local/bin/prodigal")
        os.chmod("/usr/local/bin/prodigal", 755)
        con.print(":hammer: Set up [green]prodigal[/green].")
    else:
        con.print(
            ":fearful: This does not look like Colab, I better not touch anything.")
