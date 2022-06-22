import os
import pandas as pd
import click
from sklearn.model_selection import train_test_split


@click.command("split")
@click.option("--input-dir")
@click.option("--output-dir")
def split(input_dir: str, output_dir):

    print("*********************************")
    X = pd.read_csv(os.path.join(input_dir, "data.csv"))
    y = pd.read_csv(os.path.join(input_dir, "target.csv"))
    
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    os.makedirs(output_dir, exist_ok=True)
    X_train.to_csv(os.path.join(output_dir, "train_data.csv"), index=False)
    X_val.to_csv(os.path.join(output_dir, "val_data.csv"), index=False)
    y_train.to_csv(os.path.join(output_dir, "train_target.csv"), index=False)
    y_val.to_csv(os.path.join(output_dir, "val_target.csv"), index=False)


if __name__ == '__main__':
    split()