from kafka import KafkaConsumer

consumer = KafkaConsumer('tpbcmp', group_id='group2', bootstrap_servers=['172.168.10.130:9092'])
for msg in consumer:
    print(msg)

