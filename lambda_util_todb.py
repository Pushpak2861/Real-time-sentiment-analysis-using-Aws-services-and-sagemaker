import json
import boto3
import ast
import pandas as pd
import io
def lambda_handler(event, context):

    s3client = boto3.client("s3")
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("sentiment-01")

    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]

    response = s3client.get_object(Bucket = bucket_name , Key = key)
    df = response["Body"].read().decode("utf-8")
    df = pd.read_csv(io.StringIO(df))

    def table_put_item(row):
        item = {
            "id":row["id"],
            "review":row["review"],
            "category":row["category"],
            "label":row["label"]
        } 
        table.put_item(Item = item)
    
    df.apply(lambda row: table_put_item(row),axis=1)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
