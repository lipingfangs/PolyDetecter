import os
import sys

def split_fasta_file(input_file, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_basename = os.path.splitext(os.path.basename(input_file))[0]

    sequences = []
    with open(input_file, "r") as input_file:
        lines = input_file.readlines()
        header, sequence = None, []
        for line in lines:
            line = line.strip()
            if line.startswith(">"):
                if header is not None:
                    sequences.append((header, ''.join(sequence)))
                header = line
                sequence = []
            else:
                sequence.append(line)
        if header is not None:
            sequences.append((header, ''.join(sequence)))

    for idx, (header, sequence) in enumerate(sequences, start=1):
        output_filename = f"{output_basename}_{idx}.fasta"
        output_path = os.path.join(output_dir, output_filename)

        with open(output_path, "w") as output_file:
            output_file.write(header + "\n")
            output_file.write(sequence + "\n")

if __name__ == "__main__":
    
    
    input_file = sys.argv[1]
    output_directory = sys.argv[2]
    split_fasta_file(input_file, output_directory)

