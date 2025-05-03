import json
import csv
import pandas as pd


# Appliances_link = "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/raw/review_categories/Appliances.jsonl.gz" -> 95.3M records
# Software_link   = "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/raw/review_categories/Software.jsonl.gz" -> 67.1M records
# Video_games_link = "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/raw/review_categories/Video_Games.jsonl.gz" -> 137.3M records

def file_writer():
    limit = 50000
    infiles = ["Appliances.jsonl\Appliances.jsonl" ,"Software.jsonl\Software.jsonl" , "Video_Games.jsonl\Video_Games.jsonl" ]
    outfiles = ["sampled\Appliances.jsonl" ,"sampled\Software.jsonl" , "sampled\Video_Games.jsonl"]
    for i in range(len(outfiles)):
        count = 0
        with open(infiles[i] , "r") as infile , open(outfiles[i] , "w") as outfile:
            for line in infile:
                if count>=limit:
                    break
                review = json.loads(line.strip())
                outfile.write(json.dumps(review)+'\n')
                count +=1
        
        print(f"loaded {limit}k files in {outfiles[i]}")

    categories = {
        "sampled\Appliances.jsonl" : "appliances",
        "sampled\Software.jsonl" : "software",
        "sampled\Video_Games.jsonl" : "video_games"
    }

    output_data = []

    for file_name , category in categories.items():
        with open(file_name , "r") as file:
            for line in file:
                review = json.loads(line.strip())
                text = review.get("text" , "")
                if text:
                    output_data.append((text , category))


    with open("csvdataset\data.csv" , "w" , encoding="utf-8", newline='') as cs:
        writer = csv.writer(cs)
        writer.writerow(["review" , "category"])
        writer.writerows(output_data)

def chunk_writer():
    df = pd.read_csv(r'csvdataset\data.csv')
    df["id"] = range(len(df))

    df = df.sample(frac=1 , random_state=42 ).reset_index(drop=True) # --> it will drop the old index and give you new index after shuffling
    col = df.columns
    chunk_len = 100
    chunks = [df[i:i+chunk_len] for i in range(0,len(df),chunk_len)]

    count =0
    for ch in chunks:
        ch.to_csv(f"chunk_files\chunk{count}.csv" , columns=col , index= False)
        count+=1

if __name__ == "__main__":
    file_writer()
    chunk_writer()




        

