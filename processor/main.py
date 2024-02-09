
import pandas as pd
import json
import pathlib

def find_columns_to_flatten(df: pd.DataFrame, dtype):
    return [col for col in df.columns if all(isinstance(cell, dtype) for cell in df[col])]

def flatten_nested_json_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.reset_index(drop=True)
    
    list_columns = find_columns_to_flatten(df, list)
    dict_columns = find_columns_to_flatten(df, dict)
    
    while list_columns or dict_columns:
        for col in dict_columns:
            # Explode dictionaries horizontally by adding new columns
            horiz_exploded = pd.json_normalize(df[col]).add_prefix(f'{col}.')
            df = pd.concat([df.drop(columns=[col]), horiz_exploded], axis=1)
        
        for col in list_columns:
            # Explode lists vertically
            df = df.explode(col)
        
        # Re-evaluate columns after modification
        list_columns = find_columns_to_flatten(df, list)
        dict_columns = find_columns_to_flatten(df, dict)
    
    return df


def parse_json_df(json_obj):
    list_of_dataframes = []
    try:
        data = pd.DataFrame().from_dict(json_raw)
        list_of_dataframes.append(data)
    except ValueError:
        if isinstance(json_raw, dict):
            try:
                for key in json_raw.keys():
                    tmp = pd.DataFrame().from_dict(json_raw[key])
                    flat_tmp = flatten_nested_json_df(tmp)
                    list_of_dataframes.append(flat_tmp)
            except Exception as exp:
                print(exp)
    return list_of_dataframes



        
def get_path_root(path:str):
    path_obj = pathlib.Path(path)
    return str(path_obj.parent.parent)

def handler(path:str):
    root = get_path_root(path)
    with open(path, 'r+') as f:
        json_raw = json.load(f)
    data = parse_json_df(json_raw)

    for i, pdf in enumerate(data):
        pdf.to_csv(f'{root}/csv/{i}.csv', index=False)

if __name__ == "__main__":
    handler(path='./DATA/json/city_love_list.json')


