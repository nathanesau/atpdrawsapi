# hack since pytest doesn't like absolute imports
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__)))

import boto3
import draw_parser
import dynamo_writer
import json

BUCKET = 'atpdraws'

def read_record(s3_client, record):
    s3_record = record["s3"]
    bucket = s3_record["bucket"]["name"]
    key = s3_record["object"]["key"]
    object = s3_client.Object(bucket_name=bucket, key=key)
    content = object.get()['Body'].read().decode('utf-8')
    return content

def handler(event, _):
    """
    # handle draw_added events for BUCKET
    """
    session = boto3.Session()
    s3_client = session.resource('s3')
    records = event["Records"]
    for record in records:
        content = read_record(s3_client, record)
        draw = draw_parser.parse_draw(content)
        dynamo_writer.create_or_update_draw(draw=draw, session=session)
        print("wrote draw to dynamo for event: " + json.dumps(event))
    return {"tournament_name": draw.tournament.name, "tournament_start_date": draw.tournament.start_date,
            "tournament_end_date": draw.tournament.end_date}
