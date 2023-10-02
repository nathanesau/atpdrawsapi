import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import { PythonLayerVersion } from '@aws-cdk/aws-lambda-python-alpha';
// import * as sqs from 'aws-cdk-lib/aws-sqs';

export class LambdaStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const depsLayer = new PythonLayerVersion(this, 'PythonDependencyLayer', {
        layerVersionName: 'python-dependency-layer',
        entry: '..',
        compatibleRuntimes: [lambda.Runtime.PYTHON_3_9],
        bundling: {
            assetExcludes: ['.*', '*.md', '*.json', '*.js', '*.py', 'bin/', 'lib/', 'src/', 'test/', 'cdk.out/', 'node_modules/'],
        }
    });

    // Lambda function for updating Matchup table
    const helloLambda = new lambda.Function(this, "ParserLambda", {
        functionName: 'parser-lambda',
        runtime: lambda.Runtime.PYTHON_3_9,
        code: lambda.Code.fromAsset('../src'),
        handler: 'parser.handler',
        layers: [depsLayer]
    });
  }
}
