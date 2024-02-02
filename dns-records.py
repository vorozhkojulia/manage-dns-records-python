import module_data
import boto3

client = boto3.client('route53')

def create_cname_record(hosted_zone_id, record_name, record_value):
    
    change_batch = {
        'Changes': [
            {
                'Action': 'CREATE',
                'ResourceRecordSet': {
                    'Name': record_name,
                    'Type': 'CNAME',
                    'TTL': 300,
                    'ResourceRecords': [{'Value': record_value}]
                }
            }
        ]
    }

    response = client.change_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        ChangeBatch=change_batch
    )


# hosted_zone_id = 'Z0328324FEQV8PQN4U7Z'
# record_name = 'git.julia.vorozhko.net'
# record_value = 'wordpress-alb-1198508628.us-east-1.elb.amazonaws.com' #ResourceRecords - ALB or IP or...

#create_cname_record(hosted_zone_id, record_name, record_value)

for record_name, record_value in module_data.record_data:
    create_cname_record(module_data.hosted_zone_id, record_name, record_value)


############ List Records ###########

paginator = client.get_paginator('list_resource_record_sets')

try:
    source_zone_records = paginator.paginate(HostedZoneId='Z0328324FEQV8PQN4U7Z')
    for record_set in source_zone_records:
        for record in record_set['ResourceRecordSets']:
            if record['Type'] == 'CNAME':
                print(record['Name'])

except Exception as error:
    print('An error occurred getting source zone records:')
    print(str(error))
    raise