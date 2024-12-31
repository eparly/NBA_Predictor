import { Bucket } from 'aws-cdk-lib/aws-s3'
import { Table, TableProps, Attribute, AttributeType } from 'aws-cdk-lib/aws-dynamodb'
import { Construct } from 'constructs'
import { CfnOutput, Duration, Stack, StackProps } from 'aws-cdk-lib'
import { Queue } from 'aws-cdk-lib/aws-sqs'


export class StatefulStack extends Stack {
	public readonly NbaBucket: Bucket
	public readonly NbaTable: Table
	public readonly predictionQueue: Queue
	public readonly oddsQueue: Queue
  	constructor(scope: Construct, id: string, props?: StackProps) {
		super(scope, id, props)
		
		const partitionKey: Attribute = {
			name: 'date',
			type: AttributeType.STRING
		}

		const sortKey: Attribute = {
			name: 'type-gameId',
			type: AttributeType.STRING
		}
			
		const tableProps: TableProps = {
			partitionKey,
			sortKey,
			tableName: 'NbaTable'
		}

    	// S3 Bucket
    	this.NbaBucket = new Bucket(this, 'NbaBucket')
		this.NbaTable = new Table(this, 'NbaTable', tableProps)
		this.predictionQueue = new Queue(this, 'PredictionsQueue', {
			visibilityTimeout: Duration.minutes(10)
		})
		this.oddsQueue = new Queue(this, 'OddsQueue', {
			visibilityTimeout: Duration.minutes(10)
		})
		
		new CfnOutput(this, 'NbaBucketName', {
			value: this.NbaBucket.bucketName,
			exportName: 'NbaBucketName'
		})
			
		new CfnOutput(this, 'NbaTableName', {
			value: this.NbaTable.tableName,
			exportName: 'NbaTableName'
		})
			
  }
}
