'''
1/ script A
Le script devra demander à l'utilisateur le nombre de vms à créer.

Chaque VM:
- sera instanciée à partir de l'image ubuntu 20.04, t2.micro, volume par défaut, vpc par défault
- lancera un serveur apache2 sous une forme conteneurisée (Docker)
'''
#import du module pour communiquer avec AWS
import boto3

#fonction pour récupérer l'id des instances
def get_id_instances():
    ec2_client = boto3.client("ec2")
    reservations = ec2_client.describe_instances(Filters=[
        {
            "Name": "instance-state-name",
            "Values": ["running"],
        }
    ]).get("Reservations")

    id_list=[]
    for reservation in reservations:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]
            # instance_type = instance["InstanceType"]
            # public_ip = instance["PublicIpAddress"]
            # private_ip = instance["PrivateIpAddress"]
            id_list.append(instance_id)
            # print(f"{instance_id}, {instance_type}, {public_ip}, {private_ip}")

    return id_list


#boucle while pour redemander la saisie en cas d'erreur
while True:
    try:
        #demande à l'utilisateur le nombre de VM à créer
        n=int(input('Nombre de VM ? '))
        client = boto3.client('ec2')

        #création des instances
        response = client.run_instances(
            ImageId='ami-0a49b025fffbbdac6',
            InstanceType='t2.micro',
            MinCount=0,
            MaxCount=n
        )

        #indique le nombre de VM créées
        if n==1 :
            print(f"{n} VM a été créée")
        else:
            print(f"{n} VM ont été créées")

        #récupérer l'id d'une instance en cours de création
        wait_instance_id = response["Instances"][0]["InstanceId"]

        #attend que l'instance soit en status "running"
        waiter = client.get_waiter('instance_running')
        waiter.wait(InstanceIds=[wait_instance_id])
        instance_id=get_id_instances()
        print(instance_id)

        #écrit les id des instances dans un fichier texte
        f = open("instanceid.txt", "w")
        for element in instance_id:
            f.write(element + "\n")
        f.close()

        break

    
    #Message d'erreur en cas de mauvaise saisie
    except ValueError:
        print('Erreur: Valeur non valide')

    #Autre erreur
    except:
        print ('Erreur')




