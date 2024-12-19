import csv

def process_csv(input_filepath, output_filepath):
    """
    Reads a CSV file, adds a new calculated column (integer), and writes to a new CSV.

    Args:
        input_filepath (str): The path to the input CSV file.
        output_filepath (str): The path to save the modified CSV file.
    """
    try:
        with open(input_filepath, 'r', newline='') as infile, \
                open(output_filepath, 'w', newline='') as outfile:

            reader = csv.reader(infile)
            writer = csv.writer(outfile)

            header = next(reader)
            

            try:
                usd_proposed_value_index = header.index('usd_proposed_value')
            except ValueError:
                print("Error: 'usd_proposed_value' column not found in CSV.")
                return


            header.insert(usd_proposed_value_index + 1, 'use_proposed_value_mtco2e')
            writer.writerow(header)

            for row in reader:
                try:
                    usd_value = float(row[usd_proposed_value_index])
                    mtco2e_value = int(usd_value * 1000000)  # Calculate and convert to integer
                    row.insert(usd_proposed_value_index + 1, mtco2e_value)
                    writer.writerow(row)

                except (ValueError, IndexError) as e:
                    print(f"Error processing row: {row}.  Error:{e}")
                    continue
               
        print(f"Successfully processed and saved to {output_filepath}")
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_filepath}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    input_file = "/home/daniel/Git/Emissions-Monetisation-Calculator/proposals/versions/v2.csv"
    output_file = "/home/daniel/Git/Emissions-Monetisation-Calculator/proposals/versions/v3.csv"
    process_csv(input_file, output_file)