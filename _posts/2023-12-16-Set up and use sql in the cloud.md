---
layout: post
title:  "Set up and use SQL in the cloud"
tags: data tutorial
---

# Set up and use SQL in the cloud
Most people have limits on the computational capacity they have access to.
Here I'll describe steps to set up a SQL database on the cloud where, instead of paying for a brand new computer, one can pay only for what they use.

In the following example, I will be using a small Kaggle dataset to outline the steps which one would take to populate a SQL database and do analysis in the cloud.

You'll need to be comfortable with [Jupyter](https://jupyter.org) and [Pandas](https://pandas.pydata.org) for this tutorial.
After this tutorial, you can apply all the SQL skills you have on hand.

You can find [this notebook](https://colab.research.google.com/drive/1yJZ-16izUwepOp-6nxjPCYWeKWTgQiju?usp=sharing) which has all the code used in this tutorial.


## Download a Kaggle dataset.
Grab the following files from 
[Taxi Trip Fare Prediction](https://www.kaggle.com/datasets/nani123456789/taxi-trip-fare-prediction) on Kaggle (you'll need an account for this):

<img src="/assets/posts/2023-12-16/kaggle_files.png" alt="kaggle files" height="100"/>


## Create and enable BigQuery on Google Cloud.
Make sure you have BigQuery enabled on your Google Cloud project.
You'll need to set up a Google Cloud account (see [Getting Started](https://cloud.google.com/docs/get-started)) and [create a project](https://developers.google.com/workspace/guides/create-project).
You should see the screen below when you visit `https://console.cloud.google.com/bigquery?project=<your-project-id>`:

<img src="/assets/posts/2023-12-16/gcp_bq_main.png" alt="google cloud bigquery" height="300"/>

Otherwise, you should see a splash screen to enable BigQuery. Follow the instructions to do so.

Since we'll need to create tables for querying, we'll need to create a dataset (this is analogous to databases or schemas in SQL).
To do this, go to the BigQuery Studio page and select "Create dataset" when clicking on the dots to the right of your project name. 

<img src="/assets/posts/2023-12-16/gcp_bq_dataset_create.png" alt="create dataset in big query" height="300"/>

Let's use `taxi_fare` for "Dataset Id" and you should now see the following screen in your Explorer tab (see that `taxi_fare` is now nested below your project id):

<img src="/assets/posts/2023-12-16/gcp_bq_dataset_main.png" alt="taxi_fare dataset is now in dashboard" height="400"/>

Now we should be able to create and modify tables in the `taxi_fare` dataset.

## Ingest dataset into BigQuery.
We'll be using [Colab notebooks](https://colab.research.google.com) to do this since they have [Google Cloud SDK](https://cloud.google.com/sdk?hl=en) pre-installed so it's easy to interact with Google Cloud resources.
You can, of course install them locally.
More specifically, we'll be using the [BigQuery python client](https://cloud.google.com/python/docs/reference/bigquery/latest).

Make sure you're logged into the same Google account as your Google Cloud so that credentials are automatically populated (you'll receive a prompt to do so).

Pandas has BigQuery integration via `pandas_gbq` which makes [uploading to BigQuery a one-liner affair](https://cloud.google.com/bigquery/docs/samples/bigquery-pandas-gbq-to-gbq-simple).
The following example (run this on a Colab notebook) inserts two rows into the table `taxi_fare.test` (and deletes the table if it exists).

```python
import pandas as pd
import pandas_gbq

df = pd.DataFrame({'colA': [1,2], 'colB': [3,4]})
df.to_gbq(destination_table='taxi_fare.test', project_id='<your-project-id>', if_exists='replace')
```

Now we should see `taxi_fare.test` created and populated (try playing around with "Query" on the interface).

<img src="/assets/posts/2023-12-16/ingested_two_rows.png" alt="ingested two rows" height="300"/>


### Ingesting the Kaggle files
But the Kaggle files are on your computer! You can use the sidebar option to upload them to the Colab runtime like so (you should see the files show up below "sample_data" once you've uploaded the files): 

<img src="/assets/posts/2023-12-16/colab_upload_files.png" alt="upload files to colab" height="300"/>

These files should now be available in your working directory so the following should show you the top few rows of `train.csv`:

```python
train = pd.read_csv('train.csv')
train.head()
```

So then we can put that into BigQuery using the following command:

```python
train.to_gbq(destination_table='taxi_fare.train', project_id='<your-project-id>', if_exists='replace')
```

#### Homework
> Upload `test.csv` to the table `taxi_fare.test`.


### Gotchas
* If you're updating a table, you'll probably need to set up the table with primary keys and explicitly manage data types. This is a bit more complicated and we'll skip this for this tutorial.
* For relatively large input datasets (i.e. takes too long to upload), you'll probably need to make then into chunks and append to the destination table. You may also encounter issues similar to updating a table.


## Doing analysis in BigQuery.
We can now [read from BigQuery using Pandas](https://pandas.pydata.org/docs/reference/api/pandas.read_gbq.html) in a similar way.
The following should give you all the rows in `train.csv`:

```python
pd.read_gbq("SELECT * FROM taxi_fare.train", project_id='kaggle-390719', dialect="standard").head()
```

<img src="/assets/posts/2023-12-16/load_from_bq.png" alt="loaded from big query" height="200"/>
