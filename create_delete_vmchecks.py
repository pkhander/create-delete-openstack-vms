"""Create/Delete a vm using openstack sdk"""

import os
import time
import socket
import openstack
import os.path
from novaclient.v2.client import Client
from novaclient import client


conn = openstack.connect(cloud="kaizen_oidc")
nova_client = client.Client(2, session=conn)

SERVERNAME = "conn.connect.vm"
IMAGENAME = "centos7-1907"
FLAVOR = "m1.small"
NETWORK = "default_network"
POOL = "external"
KEYPAIR_NAME = "pk"
instance = None


def create_instance(conn):
    """Create a vm + assing floating ip + SSH in the VM"""

    try:
        image = conn.compute.find_image(IMAGENAME)
        flavor = conn.compute.find_flavor(FLAVOR)
        network = conn.network.find_network(NETWORK)
        keypair = conn.compute.find_keypair(KEYPAIR_NAME)

        instance = conn.compute.create_server(
            name=SERVERNAME,
            image_id=image.id,
            flavor_id=flavor.id,
            networks=[{"uuid": network.id}],
            key_name=keypair.name,
            timeout=600,
        )

        instance = conn.compute.wait_for_server(instance)
        print("Creation Success!!")

    except Exception as err:
        print("Creation Failed!")
        print(err)

    try:
        instance = conn.compute.wait_for_server(instance)
        ip = conn.available_floating_ip()

        conn.compute.add_floating_ip_to_server(
            server=instance.id,
            address=ip.floating_ip_address)

        print("Assign Floating Success!!")

    except Exception as err:
        print("Assign Floating Failed!")
        print(err)

    time.sleep(120)

    for i in range(0, 5):
        while True:
            try:
                test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                test_socket.connect((ip.floating_ip_address, 22))
                print("SSH Success!!")
                break
            except Exception as err:
                print("SSH Failed!")
                print(err)
                break
            else:
                test_socket.close()


def delete_instance(conn):
    """Deletes the VM + floating IP sent to the pool"""

    try:
        conn.compute.delete_server(instance, 600)
        print("Server Deleted")

    except Exception as err:
        print("Deletion failed")
        print(err)


create_instance(conn)

delete_instance(conn)
