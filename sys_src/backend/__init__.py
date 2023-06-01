
# define the handler function that the Lambda service will use an entry point

def test(symbol):
    print(symbol)
def lambda_handler(event, context):
    print(event)
   # dic = {"test": (test, event['symbol'])}
   # dic["test"][0](dic["test"][1])

context = 0
event = {"symbol": "META"}
lambda_handler(event, context)