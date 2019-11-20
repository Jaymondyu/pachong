import json
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['172.168.10.130:9092'])
for num in range(10, 26):
    body = {
        "code": "FG001",
        "data": {"fid": num}
    }
    future = producer.send('tpbcmp', key=b'my_key', value=json.dumps(body).encode('utf-8'), partition=0)
    result = future.get(timeout=10)
    print(result)
