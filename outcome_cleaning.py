import pandas as pd


def OutcomesSave(file_path):
    df = pd.read_csv(file_path)
    output_file = "cleaned_output.csv"
    df.to_csv(output_file, index=False)

    return output_file