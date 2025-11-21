"""Command-line interface for geoprior1d."""

import argparse
from .core import prior_generator


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate 1D geological prior realizations",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "input_file",
        type=str,
        help="Path to Excel input file with geological constraints"
    )

    parser.add_argument(
        "-n", "--n-realizations",
        type=int,
        default=1000,
        help="Number of realizations to generate"
    )

    parser.add_argument(
        "-d", "--depth-max",
        type=float,
        default=90,
        help="Maximum depth in meters"
    )

    parser.add_argument(
        "-s", "--depth-step",
        type=float,
        default=1.0,
        help="Depth discretization step in meters"
    )

    parser.add_argument(
        "-p", "--plot",
        action="store_true",
        help="Display visualization plots"
    )

    parser.add_argument(
        "-j", "--n-processes",
        type=int,
        default=None,
        metavar="N",
        help="Number of parallel processes (None=sequential, -1=all cores, >0=specific number)"
    )

    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        metavar="FILE",
        help="Output HDF5 filename (default: auto-generated with timestamp)"
    )

    parser.add_argument(
        "-v", "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )

    args = parser.parse_args()

    # Run prior generator (using original parameter names)
    filename, flag_vector = prior_generator(
        input_data=args.input_file,
        Nreals=args.n_realizations,
        dmax=args.depth_max,
        dz=args.depth_step,
        doPlot=1 if args.plot else 0,
        n_processes=args.n_processes,
        output_file=args.output
    )

    print(f"\nDone! Output saved to: {filename}")

    if flag_vector[0] == 1:
        print("⚠️  Warning: Max iterations exceeded. Check constraints.")


if __name__ == "__main__":
    main()
