def shift_dot_left(line):
    parts = line.split()
    if len(parts) > 0:
        first_entry = parts[0]
        # Shift the dot 9 places to the left
        shifted_entry = "{:.9f}".format(float(first_entry) / 10**9)
        # Replace the first entry with the shifted one
        parts[0] = shifted_entry
        return ' '.join(parts) + '\n'
    else:
        return line

def main(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    modified_lines = [shift_dot_left(line) for line in lines]

    with open(output_file, 'w') as f:
        f.writelines(modified_lines)

if __name__ == "__main__":
    input_file = input("Enter the path to the input file: ")
    output_file = input("Enter the path to save the modified file: ")
    main(input_file, output_file)
