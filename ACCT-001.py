from diagrams import Cluster, Diagram
from diagrams.aws.management import Organizations, Cloudtrail
from diagrams.aws.security import IAM, IAMRole
from diagrams.aws.storage import S3
from diagrams.aws.compute import EC2
from diagrams.aws.general import General

with Diagram("ACCT-001 - AWS Account Management and Security Architecture", show=False, direction="TB"):
    with Cluster("AWS Organizations"):
        orgs = Organizations("Organizations")
        with Cluster("Accounts"):
            dev = EC2("Dev")
            uat = EC2("UAT")
            prod = EC2("Prod")

        orgs - [dev, uat, prod]

    with Cluster("Root Account Security"):
        root_user = IAM("Root User")
        mfa = General("MFA")
        root_user - mfa

    with Cluster("Access Management"):
        sso = IAMRole("AWS SSO")
        sso - [dev, uat, prod]

    with Cluster("Audit and Logging"):
        cloudtrail = Cloudtrail("CloudTrail")
        with Cluster("S3 Bucket for Logs"):
            s3 = S3("S3 Bucket")
            mfa_delete = General("MFA Delete")
            versioning = General("Versioning")
            s3 - [mfa_delete, versioning]

        cloudtrail >> s3

    orgs >> sso
    root_user >> orgs
