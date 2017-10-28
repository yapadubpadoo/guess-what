import csv
import pprint
import re
import string
from collections import OrderedDict

def get_feature(message):
    feature_patterns = {
        'ด่า': r'''ช้ามาก|ใช้ไม่ได้|แย่มาก|กาก|ไม่ตอบ|แม่ง|ห่า|ห่วย
            |เสียเวลา|แมร่ง|ถุย|สัส|เหี้ย|หงุดหงิด|เบื่อ|เงียบกริบ|เหนื่อยใจ
            |เซง|เซ็ง|ผิดหวัง|เศร้า
            |แย่
            |เกลียด
            |ไม่น่ารัก|ไม่ใหว
            |เฮงซวย
            |กรุเขียม|กรูขรรม|กุเขียม
            |โดนหลอก|ไม่ได้เรื่อง
        ''',
        'คำถาม': r'''
            ทำไม|ทามมัย|ทามมาย
            |หมายความว่าไง|หมายความว่าอะไร
            |คืออะไร|อยากทราบ|อยากรู้
            |หายไปไหน|มีมั้ย
            |ที่ไหน|ที่ใหน|ที่หนัย
            |ยังไง|ทำไง|สอบถาม|ข้องใจ
            |ถามหน่อย|ได้มั้ย|ได้ไง|ได้ไหม|ได้ไม|อยู่ไหม|อยู่มั้ย|ไหน
            |คือไร|บอกหน่อย|อะไรคะ|อะไรครับ|คือเหี้ยไร|นานไปมั้ย
            |นานไปไหม|เท่าไหร|เท่าไหร่|เท่าใด|เท่าไร|ไหมค่ะ|ไหมคะ|ไหมครับ
            |อะไรค่ะ|คือราย|ใหนคัฟ|ไหนคัฟ
            |หมดเขตยังค่ะ|หมดเขตยังคะ|หมดเขตยังครับ
            |หมดยัง
            |ต่างกันยังงัย|ต่างกันยังไง|ต่างยังงัย|ต่างยังไง|ต่างตรงไหน
            |ไม่มีเหรอ|ไม่มีหรอ|มั่ยมีเหรอ|มั่ยมีหรอ|ไม่มีหรา|มั่ยมีหรา
            |มีมั้ย|มีป่าว|มีไหม|มีป่ะ|มีมะ|มีไม|มีมัย|มีหรือ|มีเหรอ
            |ฟรีไหม|ฟรีมั้ย|ฟรีเหรอ
            |หรือไม่
            |จบกัน
            |กดไรคับ|กดไรคะ|กดไง
            |ถามนิด
            |อยู่ป่าว
            |ใช่ป่าว|ใช่มั้ย|ใช่ไหม|ใช่ป่ะ|รึเปล่า|หรือเปล่า|รึปาว|หรือปาว
        ''', 
        'สาขา': r'สาขา|shop|ศูนย์',
        'inbox': r'''inbox|อินบ๊อก|อินบ๊อก|อินบล๊อค|อินบล้อค|อินบล๊อก|อินบล้อก
            |ตอบแชท|ข้อความแชท|อินบ้อก|อินบอก
        ''',
        'ย้ายค่าย': r'ย้ายค่าย|ย้ายค้าย',
        'lead': r'''สนใจ|อยากได้|อยากซื้อ|จะซื้อ|รายละเอียด|ขอราคา|ขอรายละ|อยากด้าย
            |จะไปซื้อ|ขะไปถอย|ต้องโดน|ผ่อน|ต้องจัด
            ''',
        'ร้องขอ': r'''ขอเบอ|อยากติดต่อ|อยากถาม|ขอคำแนะนำ|แนะนำหน่อย|ขอวิธี
            |รบกวนโทรกลับ|เปลี่ยนโปร|ช่วยยกเลิก|ช่วยหน่อย
            |จะเช็คเบอ|ขอทราบ|ตอบหน่อย|กดอะไร
        ''',
        'ขอบคุณ': r'ขอบคุณ|ขอบใจ',
        'ชื่นชม': r'ชอบๆ|แรงมาก|ลื่นมาก|ดีมาก|ชอบมาก|คุ้มสุด|คุ้มมาก|ประทับใจ|ใช้ง่าย|ดีมาก|ชอบตรงนี้',
        'ยกเลิกบริการ': r'จะไม่ใช้|ไม่ไหวแล้ว|ไม่ง้อ|ยกเลิก|ไม่ทน|จะเลิกใช้|เปลี่ยนค่าย',
        'signal': r'สัญญาณ',
        'internet': r'เน็ต|เน็ท|wifi|ไวไฟ|3g|4g|edge|สามจี|สี่จี|เนตพัง|กระตุก|ปิงเยอะ|หมุนติ้ว',
        'ปัญหา account': r'เงินหาย|เงินไม่เข้า|ค่าบริการ|บัญชี|ผิดปกติ|โดนระงับ|หลุดบ่อย',
        'ลูกค้าเก่า': r'ลูกค้าเก่า|ลูกค้าทรูเก่า|ลูกค้าดีแทคเก่า|ลูกค้าเอไอเอสเก่า',
        'เติมเงิน': r'เติมเงิน|วันทูคอล|เติมวัน',
        'รายเดือน': r'บิล|ค่าบริการ|ตัดบัตร'
        # 'คิดค่าบริการผิด': ''
    }
    # print("  Message, " + message)
    features_count = 0
    features_result = {}
    for feature, pattern in feature_patterns.items():
        pattern = pattern.replace("\n","").replace(" ","")
        matches = re.findall(pattern, message, flags=re.MULTILINE)
        # print("     Find, " + pattern + ', matches = ' + str(matches))
        if  len(matches) > 0:
            features_result[feature] = 1
            features_count = features_count + 1
        else:
            features_result[feature] = 0
    features_result['feature_not_found'] = 1 if features_count == 0 else 0
    return features_result

def get_label(row):
    label = {}
    if row['ด่า'] == 1 or int(row['angry.summary.total_count']) >= 1:
        label['sentiment'] = '__label__negative'
    elif row['ชื่นชม'] == 1:
        label['sentiment'] = '__label__positive'
    else:
        label['sentiment'] = '__label__neutral'

    if row['ด่า'] == 1:
        label['label'] = '__label__complain'
    elif row['ยกเลิกบริการ'] == 1 or \
        row['คำถาม'] == 1 or \
        row['ร้องขอ'] == 1 or \
        row['สาขา'] == 1:
        label['label'] = '__label__question'
    else:
        label['label'] = '__label__other'

    return label

def pre_process(message):
    result = " ".join(message.splitlines())
    translator = str.maketrans('', '', string.punctuation)
    result = result.translate(translator)


fieldnames = [
    # 'id',
    'label',
    'message',
    # 'sentiment',
    # 'reactions_all.summary.total_count',
    # 'sad.summary.total_count',
    # 'like.summary.total_count',
    # 'love.summary.total_count',
    # 'angry.summary.total_count',
    # 'haha.summary.total_count',
    # 'wow.summary.total_count',
    # 'created_time',
    # 'permalink_url',
    # 'parent_post_id',
    # 'ด่า',
    # 'คำถาม',
    # 'สาขา',
    # 'inbox',
    # 'ย้ายค่าย',
    # 'lead',
    # 'ร้องขอ',
    # 'ขอบคุณ',
    # 'ยกเลิกบริการ',
    # 'signal',
    # 'internet',
    # 'ปัญหา account',
    # 'ลูกค้าเก่า',
    # 'เติมเงิน',
    # 'รายเดือน',
    # 'ชื่นชม',
    # 'feature_not_found',
]
with open('sentiment.csv', 'w', newline='') as sentiment_csvfile:
    sentiment_writer = csv.DictWriter(
        sentiment_csvfile, 
        delimiter=',',
        quotechar='"', 
        fieldnames=fieldnames
    )
    with open('label.csv', 'w', newline='') as label_csvfile:
        label_writer = csv.DictWriter(
            label_csvfile, 
            delimiter=',',
            quotechar='"', 
            fieldnames=fieldnames
        )
        # label_writer.writeheader()

        with open('comments_no_blank.csv') as source_csvfile:
            comments_reader = csv.DictReader(
                source_csvfile, 
                delimiter=',', 
                quotechar='"'
            )
            feature_not_found = {
                'count': 0,
                'data': []
            }
            for comment in comments_reader:
                if (len(comment['message']) < 10):
                    continue;
                features = get_feature(comment['message'])
                if features['feature_not_found'] == 1:
                    feature_not_found['count'] = feature_not_found['count'] + 1
                    feature_not_found['data'].append({
                        'id': comment['id'],
                        'message': comment['message'],
                    })
                new_row = {**comment, **features}
                label = get_label(new_row)
                new_row['message'] = pre_process(new_row['message'])
                label_writer.writerow({'label':label['label'], 'message':new_row['message']})
                sentiment_writer.writerow({'label':label['sentiment'], 'message':new_row['message']})
            
            # pprint.pprint(feature_not_found)
    print("Finish")
