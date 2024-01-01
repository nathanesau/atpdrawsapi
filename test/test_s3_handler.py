from src import s3_handler

SAMPLE_EVENT = {
    "Records": [
    {
      "eventVersion": "2.1",
      "eventSource": "aws:s3",
      "awsRegion": "us-east-1",
      "eventTime": "2023-12-31T17:21:51.426Z",
      "eventName": "ObjectCreated:Put",
      "userIdentity": {
        "principalId": "<some-principal>"
      },
      "requestParameters": {
        "sourceIPAddress": "<some-ip>"
      },
      "responseElements": {
        "x-amz-request-id": "<some-request-id>",
        "x-amz-id-2": "<some-id>"
      },
      "s3": {
        "s3SchemaVersion": "1.0",
        "configurationId": "draw_added",
        "bucket": {
          "name": "atpdraws",
          "ownerIdentity": {
            "principalId": "<some-principal-id>"
          },
          "arn": "arn:aws:s3:::atpdraws"
        },
        "object": {
          "key": "2024/brisbane.html",
          "size": 292288,
          "eTag": "956a8b707306376166f05201b91bd23a",
          "versionId": "_gJbt3ELg7uZwd.zwVH3BKMDyAK1TfST",
          "sequencer": "006591A32F4C638583"
        }
      }
    }
  ]
}

# requires aws credentials - uncomment to run!
#def test_handle_draw_added():
#    s3_handler.handle_draw_added(SAMPLE_EVENT)