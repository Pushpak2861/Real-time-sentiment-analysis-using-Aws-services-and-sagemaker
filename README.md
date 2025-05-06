## AWS Real-Time Sentiment Analysis Pipeline

This project implements a fully automated real-time sentiment analysis pipeline using AWS services including Lambda, S3, SageMaker, DynamoDB, and Streamlit. It classifies customer review sentiments into five levels from Very Positive to Very Negative and supports deployment and visualization via a Dockerized Streamlit app.

## Architecture Overview

Customer uploads a CSV file containing product reviews to an S3 bucket.

AWS Lambda is triggered by this upload and extracts the review column.

Each review is sent to a Hugging Face sentiment analysis model deployed on SageMaker for real-time inference.

The sentiment results are saved to another S3 bucket as output.csv.

A second Lambda function is triggered on the new output file and writes the sentiment data into a DynamoDB table.

An IAM user with CLI-only permissions and DynamoDB access can retrieve the table contents.

The results are visualized via a Dockerized Streamlit dashboard that pulls data via AWS CLI.

## Technologies Used
AWS S3

AWS Lambda (2 triggers)

AWS SageMaker (real-time inference endpoint using Hugging Face model)

AWS DynamoDB

AWS IAM (CLI-only user)

Streamlit (for frontend dashboard)

Docker (for containerized deployment)

AWS CLI (to query DynamoDB)

## File Flow Diagram
upload.csv (S3 Bucket A) ⟶ Lambda Trigger #1 ⟶ SageMaker Endpoint ⟶ output.csv (S3 Bucket B) ⟶ Lambda Trigger #2 ⟶ DynamoDB ⟶ AWS CLI ⟶ Streamlit (Dockerized)

## Model Performance
Two models were evaluated for sentiment classification:

With 3-class reduction (Positive, Neutral, Negative): 70% similarity

With 2-class reduction (Positive vs Negative): 86% similarity

This indicates consistency across models improves as the granularity of the sentiment labels is reduced.

## Setup Instructions
Clone the repository:
```bash
git clone https://github.com/your-username/aws-sentiment-pipeline.git
cd aws-sentiment-pipeline
```
Build and run the Streamlit Docker container:
```bash
docker build -t sentiment-dashboard .
docker run -p 8501:8501 sentiment-dashboard
```
(Optional) Use AWS CLI with IAM user credentials to test DynamoDB access:
```bash
aws dynamodb scan --table-name SentimentResults --region your-region
```

##  Streamlit Features
Dashboard displaying sentiment distribution

Category-wise sentiment filter

Option to download or export processed data

## Future Enhancements
Integrate time-series sentiment trend analysis

Add support for multiple product categories

Auto-archive processed reviews for audit logging

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
