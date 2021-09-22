"""A fake CARVEME that just gets cached models."""

from .utils import download, gunzip, con
import argparse
import os
import requests
from tempfile import TemporaryFile

assembly = os.environ["ASSEMBLY"]
model_url = (
    "https://github.com/Gibbons-Lab/2021_microbiome_course_data/"
    "raw/main/data/carveme_models/{}.xml.gz"
).format(assembly)
log_url = model_url = (
    "https://github.com/Gibbons-Lab/2021_microbiome_course_data/"
    "raw/main/data/carveme_models/{}.log"
).format(assembly)


def maincall(**args):
    """Download the model and log and print the output."""
    logs = requests.get(log_url).text
    with TemporaryFile(suffix="xml.gz") as tfile:
        download(model_url, str(tfile))
        gunzip(str(tfile), args["outfile"])
    con.print(":robot: I'm not the real CARVEME, but will pretend that I am now...")
    con.print(logs)


def main():
    """Execute argument parser."""

    parser = argparse.ArgumentParser(description="Reconstruct a metabolic model using CarveMe",
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('input', metavar='INPUT', nargs='+',
                        help="Input (protein fasta file by default, see other options for details).\n" +
                             "When used with -r an input pattern with wildcards can also be used.\n" +
                             "When used with --refseq an NCBI RefSeq assembly accession is expected."
                        )

    input_type_args = parser.add_mutually_exclusive_group()
    input_type_args.add_argument('--dna', action='store_true', help="Build from DNA fasta file")
    input_type_args.add_argument('--egg', action='store_true', help="Build from eggNOG-mapper output file")
    input_type_args.add_argument('--diamond', action='store_true', help=argparse.SUPPRESS)
    input_type_args.add_argument('--refseq', action='store_true', help="Download genome from NCBI RefSeq and build")

    parser.add_argument('--diamond-args', help="Additional arguments for running diamond")

    parser.add_argument('-r', '--recursive', action='store_true', dest='recursive',
                        help="Bulk reconstruction from folder with genome files")

    parser.add_argument('-o', '--output', dest='output', help="SBML output file (or output folder if -r is used)")

    univ = parser.add_mutually_exclusive_group()
    univ.add_argument('-u', '--universe', dest='universe', help="Pre-built universe model (default: bacteria)")
    univ.add_argument('--universe-file', dest='universe_file', help="Reaction universe file (SBML format)")

    sbml = parser.add_mutually_exclusive_group()
    sbml.add_argument('--cobra', action='store_true', help="Output SBML in old cobra format")
    sbml.add_argument('--fbc2', action='store_true', help="Output SBML in sbml-fbc2 format")

    parser.add_argument('-n', '--ensemble', type=int, dest='ensemble',
                        help="Build model ensemble with N models")

    parser.add_argument('-g', '--gapfill', dest='gapfill',
                        help="Gap fill model for given media")

    parser.add_argument('-i', '--init', dest='init',
                        help="Initialize model with given medium")

    parser.add_argument('--mediadb', help="Media database file")

    parser.add_argument('-v', '--verbose', action='store_true', dest='verbose', help="Switch to verbose mode")
    parser.add_argument('-d', '--debug', action='store_true', dest='debug',
                        help="Debug mode: writes intermediate results into output files")

    parser.add_argument('--soft', help="Soft constraints file")
    parser.add_argument('--hard', help="Hard constraints file")

    parser.add_argument('--reference', help="Manually curated model of a close reference species.")

    parser.add_argument('--default-score', type=float, default=-1.0, help=argparse.SUPPRESS)
    parser.add_argument('--uptake-score', type=float, default=0.0, help=argparse.SUPPRESS)
    parser.add_argument('--soft-score', type=float, default=1.0, help=argparse.SUPPRESS)
    parser.add_argument('--reference-score', type=float, default=0.0, help=argparse.SUPPRESS)

    parser.add_argument('--blind-gapfill', action='store_true', help=argparse.SUPPRESS)

    args = parser.parse_args()

    if args.gapfill and args.ensemble:
        parser.error('Gap fill and ensemble generation cannot currently be combined (not implemented yet).')

    if (args.soft or args.hard) and args.ensemble:
        parser.error('Soft/hard constraints and ensemble generation cannot currently be combined (not implemented yet).')

    if args.mediadb and not args.gapfill:
        parser.error('--mediadb can only be used with --gapfill')

    if args.recursive and args.refseq:
        parser.error('-r cannot be combined with --refseq')

    if args.egg:
        input_type = 'eggnog'
    elif args.dna:
        input_type = 'dna'
    elif args.diamond:
        input_type = 'diamond'
    elif args.refseq:
        input_type = 'refseq'
    else:
        input_type = 'protein'

    if args.fbc2:
        flavor = 'fbc2'
    elif args.cobra:
        flavor = 'cobra'
    else:
        flavor = config.get('sbml', 'default_flavor')

    if not args.recursive:
        if len(args.input) > 1:
            parser.error('Use -r when specifying more than one input file')

    maincall(
        inputfile=args.input[0],
        input_type=input_type,
        outputfile=args.output,
        diamond_args=args.diamond_args,
        universe=args.universe,
        universe_file=args.universe_file,
        ensemble_size=args.ensemble,
        verbose=args.verbose,
        debug=args.debug,
        flavor=flavor,
        gapfill=args.gapfill,
        blind_gapfill=False,
        init=args.init,
        mediadb=args.mediadb,
        default_score=args.default_score,
        uptake_score=args.uptake_score,
        soft_score=args.soft_score,
        soft=args.soft,
        hard=args.hard,
        reference=args.reference,
        ref_score=args.reference_score
    )


if __name__ == '__main__':
    main()
