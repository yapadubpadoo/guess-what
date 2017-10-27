import pika

def get_rabbit_channel(user, password, host, port):
    credentials = pika.PlainCredentials(user, password)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host,
                                port=int(port),
                                credentials=credentials,
                                socket_timeout=10))
    channel = connection.channel()
    return channel