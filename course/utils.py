"""Some helpers for the course."""

import gzip
import pandas as pd
import os
import requests
import shutil
from hashlib import sha256
from rich.console import Console

num_genomes = 950
assemblies = pd.read_csv("data/curated_assemblies.csv")
assembly_url = (
    "https://github.com/Gibbons-Lab/2021_microbiome_course_data/"
    "raw/main/data/contigs/{}.fna.gz"
)
prefix_map = pd.Series({
    "d": "domain",
    "p": "phylum",
    "c": "class",
    "o": "order",
    "f": "family",
    "g": "genus",
    "s": "species"
})
con = Console()
secret_names = {
    "Christian Diener": 951,
    "Priyanka Baloni": 952,
    "Noa Rappaport": 953,
    "Sean Gibbons": 954,
    "Joey Petosa": 955,
    "Alex Carr": 956,
    "Tomasz Wilmanski": 957
}


def download(url, filename):
    """Download a URL to a file."""
    req = requests.get(url, stream=True)
    with open(filename, 'wb') as f:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()


def gunzip(infile, outfile):
    """Extract gzipped file."""
    with gzip.open(infile, "rb") as inf, open(outfile, "wb") as outf:
        shutil.copyfileobj(inf, outf)


def gimme_genome(name):
    """Return a genome for the given name.

    Arguments
    ---------
    name : str
        Your name or nickname. Make it long and unique.

    Returns
    -------
    Nothing, but prints a lot of info and downloads your genome assembly.

    """
    if name == "[YOUR NAME]":
        con.print("Ehem, I do need you to input your name... :raised_eyebrow:")
        return

    if name not in secret_names:
        magic_number = int(sha256(name.encode).hexdigest(), 16) % num_genomes
        con.print("Hi, {}! Welcome to the course :tada:".format(name))
    else:
        magic_number = secret_names[name]
        con.print("Oooh, you are an instructor :star_struck: Thanks for helping out!")

    os.environ["MAGIC_NUMBER"] = str(magic_number)
    assembly = assemblies.iloc[magic_number]
    os.environ["ASSEMBLY"] = assembly["assembly"]
    species = assembly["species"]
    taxa = pd.Series({
        prefix_map[s.split("__")[0]]: s.split("__")[1]
        for s in assembly["classification"].str.split(";")
    })
    try:
        download(assembly_url.format(assembly), "data/{}.fna".format(assembly))
    except Exception:
        con.print(
            "[orange]Uh oh, looks like something went wrong downloading. "
            "Just run the cell again and everything should work :smile:."
            )
        return
    con.print("Saved the assembly to [green]data/{}.fna[/green].".format(assembly))
    con.print(
        "Wow! Your assembly is [green]{assembly}[/green] which is "
        "[green]{species}[/green] :exploding_head: \n"
        "By the way, the full GTDB taxonomic assignment is {gtdb} :nerd_face:".format(
            assembly=assembly, species=species, gtdb=" | ".join(taxa)
        )
    )
    return assembly
