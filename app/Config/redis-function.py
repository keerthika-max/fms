# redis_function.py
import redis

# Connect to the Redis server
client = redis.Redis(
    host='127.0.0.1',
    port=6379,
)

def connect_to_redis():
    try:
        # Test the connection
        client.ping()
        print('Connected to Redis')
    except redis.ConnectionError as error:
        print(f'Error connecting to Redis: {error}')

# Call the connection function to test the connection
connect_to_redis()

# Optionally, you can define additional functions to interact with Redis
def get_client():
    return client
