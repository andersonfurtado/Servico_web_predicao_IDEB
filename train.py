from sklearn.linear_model import LinearRegression
import argparse
import os
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
import joblib
from sklearn.model_selection import train_test_split
import pandas as pd
from azureml.core.run import Run#1
from azureml.core import Workspace
from azureml.data.dataset_factory import TabularDatasetFactory
from azureml.core import Dataset



# TODO: Create TabularDataset using TabularDatasetFactory
ws = Workspace.from_config()
data = ws.get_default_datastore()
path = "data/Train.csv"
try:
    ideb_dataset = Dataset.get_by_name(ws, name="dataset2019ideb")
except:
    datastore.upload('data', target_path='data')
    # Create TabularDataset & register in workspace
    ideb_dataset = Dataset.Tabular.from_delimited_files([(datastore, path)])
    ideb_dataset = ideb_dataset.register(
        ws, name="ideb_dataset", create_new_version=True,
        description="Dataset for ideb prediction"
    )


run = Run.get_context()

def clean_data(data):
   
    x_df = data.to_pandas_dataframe()
    
    y_df = x_df.pop("IDEB_2019")

    return x_df,y_df


x, y = clean_data(ideb_dataset)

# TODO: Split data into train and test sets.
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=403,shuffle=True) # 1 

run = Run.get_context()

def main():
    # Add arguments to script
    parser = argparse.ArgumentParser()
    
    #parser.add_argument("--C", type=float, default=1.0, help="Inverse of regularization strength. Smaller values cause stronger regularization")
    #parser.add_argument("--max_iter", type=int, default=100, help="Maximum number of iterations to converge")

    parser.add_argument("--kernel", type=float, default=1.0, help="Inverse of regularization strength. Smaller values cause stronger regularization")
    parser.add_argument("--penalty", type=int, default=100, help="Maximum number of iterations to converge")

    primary_metric_name='r2_score'
    args = parser.parse_args()

    #run.log("Regularization Strength:", np.float(args.C))
    #run.log("Max iterations:", np.int(args.max_iter))

    run.log("Regularization Strength:", np.float(args.kernel))
    run.log("Max iterations:", np.int(args.penalty))

    #model = LogisticRegression(C=args.C, max_iter=args.max_iter).fit(x_train, y_train)
    #joblib.dump(model,'outputs/model.joblib')
    #accuracy = model.score(x_test, y_test)

    model = LogisticRegression(kernel=args.kernel, penalty=args.penalty).fit(x_train, y_train)
    joblib.dump(model,'outputs/model.joblib')
    accuracy = model.score(x_test, y_test)
    
    run.log('r2_score', np.float(accuracy))
if __name__ == '__main__':
    main()
