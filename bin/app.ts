#!/usr/bin/env node
import 'source-map-support/register'

import { StatefulStack } from '../lib/StatefulStack'
import { App } from 'aws-cdk-lib'
import { LambdaStack } from '../lib/LambdaStack'
import { FrontendStack } from '../lib/FrontendStack'

const app = new App()
const statefulStack = new StatefulStack(app, 'StatefulStack')
const lambdaStack = new LambdaStack(app, 'LambdaStack', {
    bucket: statefulStack.NbaBucket,
    table: statefulStack.NbaTable,
    predictionsQueue: statefulStack.predictionQueue
})
lambdaStack.addDependency(statefulStack)

const frontendStack = new FrontendStack(app, 'FrontendStack', {
    env: {
        account: '498430199007',
        region: 'ca-central-1'
    }
})