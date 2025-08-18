#!/usr/bin/env python3
import boto3
import sys
import re

def get_route53_records(hostname):
    """Get Route53 records and identify service type"""
    try:
        route53 = boto3.client('route53')
        
        # List all hosted zones
        zones = route53.list_hosted_zones()['HostedZones']
        
        for zone in zones:
            zone_name = zone['Name'].rstrip('.')
            if hostname.endswith(zone_name):
                zone_id = zone['Id']
                
                # Get records for this zone
                records = route53.list_resource_record_sets(HostedZoneId=zone_id)
                
                for record in records['ResourceRecordSets']:
                    record_name = record['Name'].rstrip('.')
                    
                    if record_name == hostname:
                        if record['Type'] == 'A' and 'AliasTarget' in record:
                            alias_target = record['AliasTarget']['DNSName']
                            service_type = identify_service(alias_target)
                            return {
                                "hostname": hostname,
                                "alias_target": alias_target,
                                "service_type": service_type,
                                "record_type": "A (Alias)"
                            }
                        elif record['Type'] == 'CNAME':
                            cname = record['ResourceRecords'][0]['Value']
                            service_type = identify_service(cname)
                            return {
                                "hostname": hostname,
                                "alias_target": cname,
                                "service_type": service_type,
                                "record_type": "CNAME"
                            }
        
        return {"error": "No Route53 record found"}
    
    except Exception as e:
        return {"error": str(e)}

def identify_service(target):
    """Identify AWS service type from target"""
    if "elb.amazonaws.com" in target:
        if re.search(r'[a-z0-9]+-\d+\.', target):
            return "NLB"
        else:
            return "ALB"
    elif "cloudfront.net" in target:
        return "CloudFront"
    elif "s3-website" in target:
        return "S3 Website"
    return "Unknown"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 dns_resolver_boto3.py <hostname>")
        sys.exit(1)
    
    hostname = sys.argv[1]
    result = get_route53_records(hostname)
    
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Hostname: {result['hostname']}")
        print(f"Record Type: {result['record_type']}")
        print(f"Target: {result['alias_target']}")
        print(f"Service Type: {result['service_type']}")
