import csv
import pprint
import re

def get_feature(message):
    feature_patterns = {
        'ด่า': r'ช้ามาก|ใช้ไม่ได้|แย่มาก|กาก|ไม่ตอบ|แม่ง|ห่า|ห่วย|เสียเวลา|แมร่ง|ถุย|สัส',
        'คำถาม': r'ทำไม|หมายความว่าไง|คืออะไร|อยากทราบ|อยากรู้|หายไปไหน|มีมั้ย|ที่ไหน|ยังไง|ทำไง|สอบถาม|ข้องใจ|ถามหน่อย|ได้มั้ย|ได้ไง|ได้ไหม|ได้ไม|อยู่ไหม|อยู่มั้ย', 
        'สาขา': r'สาขา|shop|ศูนย์',
        'inbox': r'inbox|อินบ๊อก|อินบ๊อก|อินบล๊อค|อินบล้อค|อินบล๊อก|อินบล้อก|ตอบแชท',
        'ย้ายค่าย': r'ย้ายค่าย'
    }
    features_result = {}
    print("  Message, " + message)
    for feature, pattern in feature_patterns.items():
        matches = re.match(pattern, message, flags=re.MULTILINE)
        print("     Find, " + pattern + ', matches = ' + str(matches))
        if  matches is not None:
            features_result[feature] = 1
        else:
            features_result[feature] = 0
    return features_result


fieldnames = [
    'id',
    'message',
    'label',
    'sentiment',
    'reactions_all.summary.total_count',
    'sad.summary.total_count',
    'like.summary.total_count',
    'love.summary.total_count',
    'angry.summary.total_count',
    'haha.summary.total_count',
    'wow.summary.total_count',
    'created_time',
    'permalink_url',
    'parent_post_id',
    'ด่า',
    'คำถาม',
    'สาขา',
    'inbox',
    'ย้ายค่าย'
]
    
with open('processed_comments.csv', 'w', newline='') as result_csvfile:
    comment_writer = csv.DictWriter(
        result_csvfile, 
        delimiter=',',
        quotechar='"', 
        fieldnames=fieldnames
    )
    comment_writer.writeheader()

    with open('comments_no_blank.csv') as source_csvfile:
        comments_reader = csv.DictReader(
            source_csvfile, 
            delimiter=',', 
            quotechar='"'
        )
        for comment in comments_reader:
            features = get_feature(comment['message'])
            print(comment['id'])
            print(features)
            comment_writer.writerow({**comment, **features})
