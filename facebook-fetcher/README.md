#guess-what

## Data source
- DTAC, 182638887068
- TruemoveH, 204234332938286
- AIS, 127434041553

To send job to worker, use the format below
```json
{"page_id":"182638887068"}
```

## Export CSV
```bash
mongoexport --ssl --host=:ip --username=:user --password=:pass --authenticationDatabase=admin --db=:db --collection=:collection --type=csv --fields="id,message,reactions_all.summary.total_count,sad.summary.total_count,like.summary.total_count,love.summary.total_count,angry.summary.total_count,haha.summary.total_count,wow.summary.total_count,created_time,permalink_url,parent_post_id"
```
