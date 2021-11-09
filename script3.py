'''
3/ script C
Le script devra "terminer" les instances générées par le script A
'''

import boto3

#fonction pour supprimer une instance
def terminate_instance(instance_id):
    ec2_client = boto3.client("ec2")
    response = ec2_client.terminate_instances(InstanceIds=[instance_id])
    print(response)

#Ouverture du service EC2
ec2 = boto3.client('ec2')

#lecture du fichier contenant les id des instances et suppression des instances
with open("instanceid.txt") as f:
    ids = f.read().splitlines()
    print(ids)
    for i in ids:
        terminate_instance(i)