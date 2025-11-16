def correct_time(data_file, speed):
    corrected_data = []

    with open(data_file, 'r') as file:
        lines = file.readlines()

        # Extracting time and other data
        for line in lines:
            parts = line.split()
            time = float(parts[0])
            movement_x = float(parts[1])
            movement_y = float(parts[3])

            # Calculate the corrected time
            corrected_time = time + (movement_x**2 + movement_y**2)**0.5 / speed

            # Append corrected data
            corrected_data.append((corrected_time,) + tuple(parts[1:]))

    return corrected_data

def write_corrected_data(corrected_data, output_file):
    with open(output_file, 'w') as file:
        for row in corrected_data:
            file.write(' '.join(map(str, row)) + '\n')

if __name__ == "__main__":
    data_file = "wokol_osiedla.txt"  # Update with your file name
    output_file = "corrected_data_wklosiedla.txt"  # Update with your desired output file name
    speed = 0.862  # Update with the movement speed in meters per second

    corrected_data = correct_time(data_file, speed)
    write_corrected_data(corrected_data, output_file)
    print("Data correction completed. Corrected data saved to:", output_file)
