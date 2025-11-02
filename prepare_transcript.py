#!/usr/bin/env python3
"""
Utility script to convert or copy transcripts to the correct format.
"""

import sys
import shutil
from pathlib import Path


def copy_transcript(source: str, destination: str = None):
    """Copy transcript to data/input directory."""
    source_path = Path(source)
    
    if not source_path.exists():
        print(f"❌ Source file not found: {source}")
        return False
    
    # Default destination
    if destination is None:
        destination = Path("data/input") / source_path.name
    else:
        destination = Path(destination)
    
    # Create directory if needed
    destination.parent.mkdir(parents=True, exist_ok=True)
    
    # Copy file
    try:
        shutil.copy2(source_path, destination)
        print(f"✅ Copied transcript to: {destination}")
        return True
    except Exception as e:
        print(f"❌ Error copying file: {e}")
        return False


def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python prepare_transcript.py <source_file> [destination]")
        print("\nExample:")
        print("  python prepare_transcript.py ../Agent-QuickStart/data/output/transcript.txt")
        sys.exit(1)
    
    source = sys.argv[1]
    destination = sys.argv[2] if len(sys.argv) > 2 else None
    
    success = copy_transcript(source, destination)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

