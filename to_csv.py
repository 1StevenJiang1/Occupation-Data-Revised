import pandas as pd
import gzip
import io
import os


if __name__ == "__main__":
    # Specify the path to your .dat.gz file
    cwd = os.getcwd()
    file_name = "cps_00010.dat"
    file_path = os.path.join(cwd, "ipums", file_name)

    # Read the .dat file into a DataFrame
    # You may need to adjust this step based on the structure of your data
    # For example, you may need to specify delimiter, header, column names, etc.
    df = pd.read_csv(file_path, delimiter='\t')

    # Specify the path to save the CSV file
    csv_file_path = 'csp.csv'

    # Write the DataFrame to a CSV file
    df.to_csv(csv_file_path, index=False)

    print("Conversion completed. CSV file saved as:", csv_file_path)

