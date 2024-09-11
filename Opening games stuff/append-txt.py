import os

def append_text_files(input_directory, output_file):
    # Get all .txt files in the input directory
    txt_files = [f for f in os.listdir(input_directory) if f.endswith('.txt')]
    
    # Sort the files to ensure a consistent order
    txt_files.sort()
    
    # Open the output file in append mode
    with open(output_file, 'a') as outfile:
        # Iterate through each txt file
        for txt_file in txt_files:
            file_path = os.path.join(input_directory, txt_file)
            # Open each file and append its contents to the output file
            with open(file_path, 'r') as infile:
                outfile.write(infile.read())
            # Optionally, add a newline between files
            outfile.write('\n')


input_directory = ''
output_file = 'combined_openings.txt'

append_text_files(input_directory, output_file)