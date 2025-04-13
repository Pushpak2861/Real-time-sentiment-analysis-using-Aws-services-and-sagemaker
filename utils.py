import json


limit = 100000


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

