import argparse
import csv
import exifread
import os

# Sample images in the repository folder from:
# https://github.com/ianare/exif-samples

TAG_WIDTH = 50

# Reads the EXIF data from an image
def read_exif(imgfile):
  with open(imgfile, "rb") as f:
    tags = exifread.process_file(f)
  return tags

# Write the data as CSV
def write_csv(csvfile, imgfile, tags):
  # Check if the file already exists
  csv_exists = os.path.isfile(csvfile)

  with open(csvfile, 'a', newline='', encoding='utf-8') as f:
    # CSV writer
    writer = csv.writer(f)

    # Write the header only if the file didn't exist.
    if not csv_exists:
      writer.writerow(['image', 'tag', 'value'])

    # Write the actual data
    for tag, val in tags.items():
      writer.writerow([imgfile, tag, val])

def main():
  # Args
  parser = argparse.ArgumentParser(description='Extract EXIF metadata from images.')
  # Basically what the description says
  parser.add_argument('-i', '--images', nargs='+', required=True, help='One or more image files to process.')
  parser.add_argument('-s', '--show', action='store_true', help='Display the extracted data on the console. Default: True when not writing an output file (`-o`).')
  parser.add_argument('-o', '--output', nargs='?', const='results.csv', help='Optional CSV output file. Default: `results.csv` (ALWAYS appends, never overwrites).')
  # CLI parse
  args = parser.parse_args()

  # For each image
  for imgfile in args.images:
    print(f'\n ===== Processing {imgfile} =====')

    # Read its tags
    tags = read_exif(imgfile)

    # If no metadata detected
    if not tags:
      print('No EXIF metadata found!')
      continue

    # If we're writing to the CSV
    if args.output:
      write_csv(args.output, imgfile, tags)

    # Display on the console by default if we're not writing to an output file.
    # And also when writing, if accompanied by `-s` or `--show``
    if args.show or not args.output:
      for tag, val in tags.items():
        print(f'{tag:>{TAG_WIDTH}} : {val}')

if __name__ == '__main__':
  # Examples to try:
  # python exif_extractor.py -h
  # python exif_extractor.py -i BSG1.tiff IMG_5195.HEIC Canon_40D.jpg
  # python exif_extractor.py -i BSG1.tiff IMG_5195.HEIC Canon_40D.jpg -o -s
  # python exif_extractor.py -i BSG1.tiff IMG_5195.HEIC Canon_40D.jpg -o output.csv

  main()
