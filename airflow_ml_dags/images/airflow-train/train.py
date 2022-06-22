import os
import pandas as pd
import click
import pickle
from sklearn.linear_model import LogisticRegression


@click.command("train")
@click.option("--input-dir")
@click.option("--output-dir")
def train(input_dir: str, output_dir: str):
    X_train = pd.read_csv(os.path.join(input_dir, "train_data.csv"))
    y_train = pd.read_csv(os.path.join(input_dir, "train_target.csv"))

    #os.makedirs(output_dir, exist_ok=True)
    #X_train.to_csv(os.path.join(output_dir, "train_data.csv"))
    #X_val.to_csv(os.path.join(output_dir, "val_data.csv"))
    #y_train.to_csv(os.path.join(output_dir, "train_target.csv"))
    #y_val.to_csv(os.path.join(output_dir, "val_target.csv"))
    
    clf = LogisticRegression()
    clf.fit(X_train, y_train)
    
    os.makedirs(output_dir, exist_ok=True)
    with open (os.path.join(output_dir, "model.pkl"), "wb") as f:
        pickle.dump(clf, f)

if __name__ == '__main__':
    train()