import { Bucket } from 'aws-cdk-lib/aws-s3'
import { Table, TableProps, Attribute, AttributeType } from 'aws-cdk-lib/aws-dynamodb'
import { Construct } from 'constructs'
import { Stack, StackProps } from 'aws-cdk-lib'


export class StatefulStack extends Stack {
	public readonly NbaBucket: Bucket
	public readonly NbaTable: Table
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
  }
}
