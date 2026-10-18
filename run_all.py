#!/usr/bin/env python3
"""Reproducible workflow for the Card & Krueger (1994) DiD replication.

Run from the project root:

    python run_all.py

After the raw data (data/public.csv) is in place, this script regenerates every
table and figure in results/ without any manual editing of data or code.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src import extension, figures, tables  # noqa: E402


def main() -> None:
    print("=" * 70)
    print("Card & Krueger (1994) minimum-wage DiD replication")
    print("=" * 70)

    tables.main()
    figures.main()
    extension.main()

    print("All outputs written to results/")


if __name__ == "__main__":
    main()
