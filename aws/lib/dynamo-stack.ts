import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';

export class DynamoStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const tournamentTable = new dynamodb.Table(this, 'Tournament', {
      partitionKey: {
        name: 'id',
        type: dynamodb.AttributeType.STRING,
      },
      tableName: 'Tournament',
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST
    });

    const playerTable = new dynamodb.Table(this, 'Player', {
      partitionKey: {
        name: 'id',
        type: dynamodb.AttributeType.STRING,
      },
      tableName: 'Player',
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST
    });

    const entrantTable = new dynamodb.Table(this, 'Entrant', {
      partitionKey: {
        name: 'id',
        type: dynamodb.AttributeType.STRING,
      },
      tableName: 'Entrant',
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST
    });

    entrantTable.addGlobalSecondaryIndex({
      indexName: 'tournamentIdIndex',
      partitionKey: {
        name: 'tournament_id',
        type: dynamodb.AttributeType.STRING
      },
      sortKey: {
        name: 'order',
        type: dynamodb.AttributeType.NUMBER
      }
    });

    const matchupTable = new dynamodb.Table(this, 'Matchup', {
      partitionKey: {
        name: 'id',
        type: dynamodb.AttributeType.STRING,
      },
      tableName: 'Matchup',
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST
    });
  }
}
