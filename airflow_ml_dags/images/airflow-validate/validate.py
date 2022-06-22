import os
import pandas as pd
import click
import pickle
from sklearn.metrics import classification_report


@click.command("validate")
@click.option("--input-dir")
@click.option("--model-dir")
@click.option("--output-dir")
def validate(input_dir: str, model_dir: str, output_dir: str):
    X_val = pd.read_csv(os.path.join(input_dir, "val_data.csv"))
    y_val = pd.read_csv(os.path.join(input_dir, "val_target.csv"))

    #os.makedirs(output_dir, exist_ok=True)
    #X_train.to_csv(os.path.join(output_dir, "train_data.csv"))
    #X_val.to_csv(os.path.join(output_dir, "val_data.csv"))
    #y_train.to_csv(os.path.join(output_dir, "train_target.csv"))
    #y_val.to_csv(os.path.join(output_dir, "val_target.csv"))
    
   
    with open (os.path.join(model_dir, "model.pkl"), "rb") as f:
        clf = pickle.load(f)

    pred = clf.predict(X_val)

    os.makedirs(output_dir, exist_ok=True)
    
    report_dict = classification_report(y_val, pred, output_dict=True)
    report_df = pd.DataFrame.from_dict(report_dict)
    report_df.to_csv(os.path.join(output_dir, "validation_report.csv"))
        
if __name__ == '__main__':
    validate()