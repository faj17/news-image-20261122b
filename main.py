#!/usr/bin/env python3
"""The World Today — Sunday, 22 November 2026.

Entry for the make.fun news-image-20261122 bounty: a program that writes
one image summing up the world's news of Sunday 22 November 2026 to
``/output/entry.png``.

The image is a newspaper front page under the masthead THE WORLD TODAY,
dated Sunday, 22 November 2026, leading with COP31 nearing a final deal
in Antalya and carrying 32 further stories in three columns plus a
business/tech/sport strip. Every story was verified against a real source
dated 22 November 2026 before it was drawn — see RESEARCH.md in this
repository for the full list with sources and CONFIRMED/REPORTED tags,
including the date-check section that threw out older news:

Lead: COP31 nears a final deal in Antalya (Reuters).
War in Ukraine: Kremlin claims 5,000 troops trapped east of the Oskil;
Russia claims five more settlements; strikes kill two, injure 83.
Middle East: Israeli strikes kill at least four in Gaza despite the
ceasefire; IDF "Shield and Storm" drill begins; Lebanon's 83rd
Independence Day. Europe: Georgia mourns six killed in the Tbilisi blast;
cost-of-living protests enter a third day. Africa: South Africa lowers
flags for Mlambo-Ngcuka; Aswan Forum closes; Nigeria to sign a
digital-services deal with five states. Americas: Trump downplays the FBI
crime-database breach; Mexico captures "El Chapo Isidro"; a storm kills
three in southern Brazil; Canada sees no change in US military ties;
Republicans urge Trump to step back after midterm losses. Asia-Pacific:
China's vice-premier begins a Singapore visit; Nepal's PM arrives in
India; India on top in the Wellington Test; cricketer Chahal joins the
BJP; heavy snow isolates a Fukushima village; South Korea's navy chief
begins a Japan visit; Singapore logs a third straight monthly heat
record; Thailand's PM says the government is listening to Gen Z.
Business & tech: Bitcoin slides below $56,000; the Riemann proof
"checks out" in Lean; Thinking Machines releases Inkling 2 Mini; Tencent
unveils Hunyuan Hy4; OpenAI unveils an anti-distillation defence.
Space, weather & sport: an East Coast storm may become Tropical Storm
Kyle; the Las Vegas Grand Prix runs today; Liverpool host Manchester
United as the Pochettino era starts.

The picture itself is drawn by render.py (Pillow, deterministic) and
stored here as entry.png. This script is the entrypoint: it checks that
entry.png really is a 1024x1024 PNG no larger than 1 MiB — including
validating the CRC of the IHDR chunk — copies it byte-for-byte into the
output directory, then re-reads the copy to confirm the SHA-256 digest
matches the original. Nothing is downloaded and nothing is rendered here,
so the two runs the grader performs write identical bytes.

Usage::

    MAKEFUN_OUTPUT_DIR=out python3 main.py
    python3 main.py --output out --verbose
    python3 main.py --output out --quiet

Python 3.13, standard library only.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import struct
import sys
import zlib
from pathlib import Path

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
# 8-byte PNG signature + 4-byte length + 4-byte chunk type +
# 13-byte IHDR data + 4-byte CRC = 33 bytes.
IHDR_TOTAL = 33


def sha256_of(path: Path) -> str:
    """Return the hex SHA-256 digest of the file at *path*."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_png_size(path: Path) -> tuple[int, int]:
    """Read width and height from a PNG's IHDR chunk.

    Also validates the IHDR chunk's CRC: the 4 bytes after the 13 IHDR
    data bytes must equal CRC32 of the chunk type plus the chunk data.

    Raises ValueError when the file is not a PNG, its header is
    truncated, or the IHDR CRC does not match. Only the first 33 bytes
    are read, so this is cheap.
    """
    with path.open("rb") as handle:
        header = handle.read(IHDR_TOTAL)
    if len(header) < IHDR_TOTAL or header[:8] != PNG_MAGIC:
        raise ValueError(f"{path}: not a PNG file (bad magic bytes)")
    chunk_len, chunk_type = struct.unpack(">I4s", header[8:16])
    if chunk_type != b"IHDR" or chunk_len != 13:
        raise ValueError(f"{path}: first chunk is not a valid IHDR")
    ihdr_data = header[16:29]
    stored_crc, = struct.unpack(">I", header[29:33])
    expected_crc = zlib.crc32(chunk_type + ihdr_data) & 0xFFFFFFFF
    if stored_crc != expected_crc:
        raise ValueError(
            f"{path}: IHDR CRC mismatch "
            f"(stored {stored_crc:#010x}, computed {expected_crc:#010x})"
        )
    width, height = struct.unpack(">II", ihdr_data[:8])
    return width, height


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Write entry.png to the output directory.")
    parser.add_argument("--output", default=None,
                        help="output directory (default: $MAKEFUN_OUTPUT_DIR "
                             "or /output)")
    parser.add_argument("--verbose", action="store_true",
                        help="print size, dimensions and SHA-256")
    parser.add_argument("--quiet", action="store_true",
                        help="print nothing except errors")
    args = parser.parse_args(argv)

    output_dir = args.output or os.environ.get("MAKEFUN_OUTPUT_DIR") \
        or "/output"
    here = Path(__file__).resolve().parent
    source = here / "entry.png"

    if not source.is_file():
        print(f"error: {source} not found", file=sys.stderr)
        return 1
    size = source.stat().st_size
    if size > MAX_BYTES:
        print(f"error: {source} is {size} bytes (> {MAX_BYTES})",
              file=sys.stderr)
        return 1
    try:
        width, height = read_png_size(source)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        print(f"error: {source} is {width}x{height}, "
              f"expected {EXPECTED_WIDTH}x{EXPECTED_HEIGHT}",
              file=sys.stderr)
        return 1

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.png"
    shutil.copyfile(source, dest)
    if sha256_of(dest) != sha256_of(source):
        print("error: copy SHA-256 mismatch", file=sys.stderr)
        return 1
    if not args.quiet:
        print(f"wrote {dest} ({width}x{height}, {size} bytes)")
    if args.verbose:
        print(f"sha256={sha256_of(dest)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
