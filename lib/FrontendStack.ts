import { RemovalPolicy, Stack, StackProps } from "aws-cdk-lib";
import { Certificate, CertificateValidation } from "aws-cdk-lib/aws-certificatemanager";
import { Distribution, PriceClass } from "aws-cdk-lib/aws-cloudfront";
import { S3Origin, S3StaticWebsiteOrigin } from "aws-cdk-lib/aws-cloudfront-origins";
import { ARecord, HostedZone, RecordTarget } from "aws-cdk-lib/aws-route53";
import { CloudFrontTarget } from "aws-cdk-lib/aws-route53-targets";
import { BlockPublicAccess, Bucket } from "aws-cdk-lib/aws-s3";
import { BucketDeployment, Source } from "aws-cdk-lib/aws-s3-deployment";
import { Construct } from "constructs";

export class FrontendStack extends Stack {
    constructor(scope: Construct, id: string, props: StackProps) {
        super(scope, id, props);

        const siteBucket = new Bucket(this, 'WebsiteBucket', {
            bucketName: 'ethanparliament.com',
            websiteIndexDocument: 'index.html',
            publicReadAccess: true,
            blockPublicAccess: BlockPublicAccess.BLOCK_ACLS,
            removalPolicy: RemovalPolicy.DESTROY
        })

        const s3Deployment = new BucketDeployment(this, 'DeployWebsite', {
            sources: [Source.asset('./frontend')],
            destinationBucket: siteBucket
        })

        const zone = HostedZone.fromLookup(this, 'HostedZone', {
            domainName: 'ethanparliament.com'
        })

        const certificate = Certificate.fromCertificateArn(this,
            'Certificate',
            'arn:aws:acm:us-east-1:498430199007:certificate/e95f2444-760c-4166-959e-09f868741c49'
        )

        const distribution = new Distribution(this, 'Distribution', {
            defaultBehavior: { origin: new S3StaticWebsiteOrigin(siteBucket) },
            priceClass: PriceClass.PRICE_CLASS_100,
            domainNames: ['ethanparliament.com', 'www.ethanparliament.com'],
            certificate: certificate
        })

        const aRecord = new ARecord(this, 'AliasRecord', {
            zone: zone,
            recordName: 'ethanparliament.com',
            target: RecordTarget.fromAlias(new CloudFrontTarget(distribution))
            
        })
        const alternateARecord = new ARecord(this, 'AlternateAliasRecord', {
            zone: zone,
            recordName: 'www.ethanparliament.com',
            target: RecordTarget.fromAlias(new CloudFrontTarget(distribution))
        })
    }
}