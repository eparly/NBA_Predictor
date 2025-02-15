#!/usr/bin/env node
import 'source-map-support/register'

import { StatefulStack } from '../lib/StatefulStack'
import { App } from 'aws-cdk-lib'
import { LambdaStack } from '../lib/LambdaStack'

const app = new App()
const statefulStack = new StatefulStack(app, 'StatefulStack')
const lambdaStack = new LambdaStack(app, 'LambdaStack', {
    bucket: statefulStack.NbaBucket,
    table: statefulStack.NbaTable,
    predictionsQueue: statefulStack.predictionQueue,
    oddsQueue: statefulStack.oddsQueue
})
lambdaStack.addDependency(statefulStack)
