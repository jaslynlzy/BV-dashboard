import pandas as pd
import numpy as np

def ImpactFormat(file_path):
    df = pd.read_csv(file_path)

    def convert_percentage_to_number(x):
        if isinstance(x, str) and "%" in x:
            return float(x.replace("%", "")) / 100
        return x

    df["Prevalence of HIV among children whose mothers are HIV+ve \nCSB only"] = df[
        "Prevalence of HIV among children whose mothers are HIV+ve \nCSB only"
    ].apply(convert_percentage_to_number)

    def convert_number_to_percentage(x):
        if pd.isna(x):
            return x
        elif isinstance(x, (int, float)) and "%" not in str(x):
            return f"{float(x) * 100:.2f}%"
        return x

    df["Proportion of women retained in care (HIV treatment)"] = df[
        "Proportion of women retained in care (HIV treatment)"
    ].apply(convert_number_to_percentage)

    output_file = "cleaned_impact.csv"
    df.to_csv(output_file, index=False)

    return output_file
