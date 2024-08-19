
import pandas as pd
import re
def data_cleaning(input_file):
    df = pd.read_csv(input_file, dtype=str)
    print("hello")
    df = df.applymap(lambda x: x.replace('%', '') if isinstance(x, str) else x)
    columns = [ "Indicator Performance Tracking Table (IPTT)","Unnamed: 1","Unnamed: 2","Unnamed: 3","Unnamed: 4","Unnamed: 5","Unnamed: 6","Unnamed: 7","Unnamed: 8","Unnamed: 9"]
    names = ["Indicator Level","Indicator and Definition","Overall Target","Baseline Value","Target Y1","Actual Y1","Target Y2","Actual Y2", "Target Y3","Actual Y3"]
    dc = pd.DataFrame()
    for i in range(len(columns)):
        value = df.loc[2:23, columns[i]]
        dc[names[i]] = value
    melted_target = pd.melt(dc, id_vars=["Indicator Level","Indicator and Definition","Overall Target","Baseline Value"], value_vars=["Target Y1", "Target Y2","Target Y3"], var_name='Year', value_name='Target')
    target = melted_target['Target']
    melted_actual =  pd.melt(dc, id_vars=["Indicator Level","Indicator and Definition","Overall Target","Baseline Value"], value_vars=["Actual Y1", "Actual Y2","Actual Y3"], var_name='Year', value_name='Actual')
    combined_dc = pd.merge(melted_target, melted_actual, on=["Indicator Level","Indicator and Definition","Overall Target","Baseline Value","Year"], how="right")
    combined_dc['Target'] = target
    combined_dc.replace({'Actual Y1': '2021-2022', 'Actual Y2': '2022-2023', 'Actual Y3': '2023-2024'}, inplace=True)

    for i in range(1, len(combined_dc['Indicator Level'])):
        if pd.isna(combined_dc.loc[i, 'Indicator Level']):
            combined_dc.loc[i, 'Indicator Level'] = combined_dc.loc[i - 1, 'Indicator Level']

    return combined_dc