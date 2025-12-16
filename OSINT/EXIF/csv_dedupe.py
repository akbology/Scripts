import argparse
import csv
import os

# Handles renaming existing files. We definitely don't want to destroy existing files.
# This is needed because we open a file in 'w' mode, and we don't want any destructive side-effects
def autorename(path):
  # If the input is good, it's good.
  if not os.path.exists(path):
    return path
  
  # get/the/base/path.ext
  base, ext = os.path.splitext(path)
  # If needed at all, we will try ot rename to the lowest existing_filename (n).ext
  # Starting at 2 (e.g., results (2).csv)
  count = 2

  # Keep incrementing the count until we hit something we can safely name our file to
  while True:
    new_path = f'{base} ({count}){ext}'
    if not os.path.exists(new_path):
      return new_path
    count += 1

# Deduplicates `infile`, writing to `outfile` and displaying stats as a default.
def dedupe_csv(infile, outfile, stats=True):
  # Rows seen
  seen = set()
  rows = []
  # Counter for the duplicates seen
  n_dups = 0

  # Read infile
  with open(infile, newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    # We just saw the header
    rows.append(header)

    # For each row
    for row in reader:
      # Get is tuple
      row_tuple = tuple(row)
      # If encountered before, count it as a duplicate (to remove)
      if row_tuple in seen:
        n_dups += 1
        # No writing here, guv
      else:
        # New row we just saw. Add it to seen and append it to the rows to write.
        seen.add(row_tuple)
        rows.append(row)

  # Autorename handles duplicate filenames - just in case outfile 'accidentally' exists.
  # But only if NOT inplace
  if infile != outfile:
    outfile = autorename(outfile)

  # Open the output file.
  with open(outfile, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(rows)
    # Mandatory feedback because autorename might have changed the outfile name from the original input.
    print(f'{outfile} written.')
  
  # Basic stats display
  if stats:
    print(f'{n_dups} duplicates removed.')

def main():
  # Args
  parser = argparse.ArgumentParser(description='Remove duplicate rows from a CSV file.')
  parser.add_argument('-i', '--infile', required=True, help='Input CSV file to dedupe.')
  parser.add_argument('-o', '--outfile', help='Output CSV file. Required unless --inplace is used.')
  parser.add_argument('--inplace', action='store_true', help='Overwrite the input file with the deduped output.')
  parser.add_argument('-q', '--quiet', action='store_true', help='Suppress the stats display.')
  # Parse
  args = parser.parse_args()

  # If inplace: outfile = infile
  if args.inplace:
    outfile = args.infile
    # If the user specified both --inplace and -o/--outfile,
    # Assume the safer default and let -o/--outfile take precedence
    if args.outfile:
      print('-o/--outfile detected with --inplace. Ignoring --inplace')
      outfile = args.outfile
  # -o/--outfile is required when not --inplace
  elif not args.outfile: # not --inplace and not -o/--outfile
    parser.error('-o/--outfile required when not using --inplace.')
  else: # not --inplace and yes -o/--outfile
    outfile = args.outfile

  # Deduplicate with the infile and outfile as above.
  # Show the stats if NOT quiet.
  dedupe_csv(args.infile, outfile, stats=not args.quiet)

if __name__ == '__main__':
  main()
