* Run the following commands
```bash
cd data-processor
mongoexport --ssl --host=cluster0-shard-00-00-oix69.mongodb.net --username="guess-what-mongo" --password="xxxxxxxxxx" --authenticationDatabase=xxxxxxxxxx --db=xxxxxxxxxx --collection=comments --type=csv --fields="id,message,reactions_all.summary.total_count,sad.summary.total_count,like.summary.total_count,love.summary.total_count,angry.summary.total_count,haha.summary.total_count,wow.summary.total_count,created_time,permalink_url,parent_post_id" --query="{message:{\$ne:\"\"}, message_tags:{\$exists:false}, parent_post_id:{\$not: /127434041553/}}" --out=comments_no_blank.csv
. env/bin/activate
pip install -r requirements.txt
python gen_label_and_pre_process.py
python gen_one_class_data.py
cd <path to tokenize>
python tokenize-csv.py 
rsync -rave "ssh -i <pem file>" <local_path>/*_tokenized.csv  ubuntu@<ip>:<path>
```
