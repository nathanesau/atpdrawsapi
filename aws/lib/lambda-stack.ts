import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import { Effect, PolicyStatement } from 'aws-cdk-lib/aws-iam';
import { Bucket, EventType } from 'aws-cdk-lib/aws-s3';
import { LambdaDestination } from 'aws-cdk-lib/aws-s3-notifications';
//import * as lambdaEventSources from '@aws-cdk/aws-lambda-event-sources';

export class LambdaStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const s3HandlerLambda = new lambda.Function(this, "S3HandlerLambda", {
        functionName: 's3-handler-lambda',
        runtime: lambda.Runtime.PYTHON_3_9,
        code: lambda.Code.fromAsset('../src'),
        handler: 's3_handler.handler',
        // ideally, we should use PythonLayerVersion
        // for now, the layer is manually created and referenced
        layers: [lambda.LayerVersion.fromLayerVersionArn(this,
          'bs4Layer',
          'arn:aws:lambda:us-east-1:474996171677:layer:bs4-python39:1')
        ],
        timeout: cdk.Duration.seconds(60),
    });

    s3HandlerLambda.addToRolePolicy(new PolicyStatement({
      actions: ['dynamodb:*'],
      effect: Effect.ALLOW,
      resources: ['*']
    }));

    s3HandlerLambda.addToRolePolicy(new PolicyStatement({
      actions: ['s3:*'],
      effect: Effect.ALLOW,
      resources: ['*']
    }));

    // this bucket is manually created
    // there are github actions configured to write to this bucket
    const s3Bucket = Bucket.fromBucketArn(this, "atpdrawsBucket", "arn:aws:s3:::atpdraws");
    s3Bucket.addEventNotification(EventType.OBJECT_CREATED_PUT, new LambdaDestination(s3HandlerLambda));
  }
}
