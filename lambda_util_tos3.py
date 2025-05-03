import json
import boto3
import ast
import pandas as pd
import io
def lambda_handler(event, context):
    print(event)
    endpoint_name = "sentiment-analysis-endpoint04"

    runtime_client = boto3.client("runtime.sagemaker")

    s3client = boto3.client("s3")

    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]

    response = s3client.get_object(Bucket = bucket_name , Key = key)
    df = response["Body"].read().decode("utf-8")
    df = pd.read_csv(io.StringIO(df))
    
    def predict(review):
        review = json.dumps(review)
        response = runtime_client.invoke_endpoint(
            ContentType="application/json",
            Body=review,
            EndpointName=endpoint_name
        )
        result = response["Body"].read().decode("utf-8")
        result = json.loads(result)
        result =  result[0]["label"]
        if result == "neutral":
            return "negative"
        else:
            return "positive"
    
    df["label"] = df["review"].apply(lambda rev: predict({"inputs":rev[:512]}))
    output_csv = df.to_csv(index=False, header=True, sep=",")

    s3client.put_object(Bucket = "sagemaker-eu-west-1-117572039187" , Key = "output.csv", Body = output_csv)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
