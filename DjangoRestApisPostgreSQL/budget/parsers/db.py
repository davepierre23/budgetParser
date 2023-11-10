import boto3

dynamodb = boto3.resource('dynamodb')
Transcations_table= 'Transcations'
Transcations = dynamodb.Table(Transcations_table)

from more_itertools import chunked
import boto3




#large amount of data to insert,
# to avoid hitting the DynamoDB write limits.
def saveTranscationModelBatches(df):
    client = boto3.client('dynamodb')
    # get a list of dictionaries representing each row of your dataframe
    items = df.to_dict(orient='records')

    # specify the batch size you want to use
    batch_size = 25  # for example

    # split the list of items into batches
    item_batches = chunked(items, batch_size)

    # iterate over the batches and upload each one to DynamoDB
    for batch in item_batches:
        # create a list of PutRequest objects, one for each item in the batch
        put_requests = [{'PutRequest': {'Item': item}} for item in batch]

        # create a dictionary representing the batch of items to upload
        request_items = {Transcations_table: put_requests}

        # use the batch_write_item() method to upload the batch to DynamoDB
        response = client.batch_write_item(RequestItems=request_items)

def saveTranscationModel(df, table):

    table.put_item(Item=item)
    # Insert the items into the table

    #inserts the items using the batch_write_item method,
    #More efficient than inserting them one at a time. 
    with table.batch_writer() as batch:
        for item in df:
            batch.put_item(Item=item)


    # print a success message
    print('Data has been successfully saved to DynamoDB.')



    # Define categories based on keywords in the "Description" column
categories = {
        "Wealthsimple":["Wealthsimple"],
        "Alcohol": ["LCBO/RAO"],
        "Food": [  "JACK ASTOR'S","MCDONALD'S","Seoul Dog","REXALL","PIZZERIA","COBS BREAD","MILKMAN ","SUSHI","BRIG","LEXINGTON SMOKEHOUSE",'CHICK-FIL-A' ,"KFC","FRUIT","BROADWAY","DELICIOUS STEAKHOUSE","TIM HORTONS","STARBUCKS", "LUNCHBOX","Wild Wing ", "THE ALLEY","GYUBEE","RED LOBSTER", 'MENCHIE',"SQ *PANCHO'S ", "DAOL" , "SOUL STONE","MR. PRETZEL","METROPOLITAIN",
                    "St. Louis Bar","Bagel","LE ST LAURENT","MAVERICK'S",'POPEYES', "Chatime ","SOBEYS",'SHAKER',"MARY BROWN'S","SUSHI KAN","MANDARIN", "SHOPPERS",
             "WENDY'S", 'LE MIEN',"METRO","JOLLIBEE-","MOXIES","T&T","LOBLAWS","AZTEC","GREEN FRESH","FARM BOY","TEALIVE","BOSTON PIZZA","EAST SIDE MARIO",
            "Pizza Pizza ",'THE GREAT CANADIAN PO', 'UBER EATS ', "Shoppers Drug Mart",'BIG BONE BBQ',"NSEYA'S"],
        "Wardrobe": ["Tip Top", "Shoe Company",'SP JOJIKA','SHEIN',"VALUE VILLAGE","OVO"],
        "Entertainment": [
            "NORDIK",
            "TEE 2 GREEN",
            "DOLLYS",
            "STEAM",
            "TICKET",
            "LANDMARK",
            "WHITE SANDS",
            "Orleans Bowling.com",
            "BOWLING",
            "Top Karting Hull",
            "Sunrise Records",
            "SP TSX1",
            'eBay',
            'GAMESTOP',
            "CARTA",
            'Canada Computers',
            'PLAYSTATION',
            'RED DRAGON',
            'TCGPLAYER.COM',
            "401 GAMES"
  
        ],
        'Transporation':[ "Uber ","Lyft",'PRESTO',"PPARK","BUSBUD"],
        "Doctors/dental/vision":["APPLE'S CROWN",'ACE OF SPADES',"CLEARVIEW"],
        "Beauty":["CLORE","MONTEGO","MONAT"],
        "Gym":   [ "SHOWCASE ","SP CROSSROPE",'FIT4LESS'],
        "Home goods": ["AMZN", "APPLE","Dollarama","PANDABUY","BEST BUY","DOLLAR TREE","GIANT TIGER","CDN TIRE","HUDSON'S BAY",'AMAZON','WAL-MART'],
        'Income':['Basic Pay','Acting / Appointment Pay'],
        'Gas':['PIONEER',"ULTRAMAR",'CIRCLEK',"MOBIL","GAS","PETROCAN", 'MRGAS','ESSO','SHELL',"FUEL"],
        'Church':["CALVARY CHURCH"],
        'Education':["OPTIONS"],
        "Miscellaneous Payement": [
            "Dishonoured Payment",
            "Returned Payment",
            'REFUNDED'
        ],
        "Miscellaneous Charges": [
            'MONTHLY FEES',
            "Dishonoured Payment",
            "PREMIUM"
         
        ]
    }
def insertCatergories():
    # Create a DynamoDB client
    dynamodb = boto3.resource('dynamodb')

    # Define the table name
    table_name = 'categories_table'

    # Create the table
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'category',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'description',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'category',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'description',
                'AttributeType': 'S'
            }
        ],
        BillingMode='PAY_PER_REQUEST'
    )
    # Wait for the table to be created
    table.meta.client.get_waiter('table_exists').wait(TableName=table_name)

    # Add categories to the table
    for category, keywords in categories.items():
        for keyword in keywords:
            table.put_item(Item={
                'category': category,
                'description': keyword
            })

insertCatergories()