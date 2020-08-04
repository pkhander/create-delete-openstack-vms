#!/usr/bin/env python3

"""Create/Delete a vm using openstack sdk"""


import os
import time
import socket
import logging
import openstack
import os.path
from novaclient.v2.client import Client
from novaclient import client


CLOUDNAME = "kaizen_oidc"
SERVERNAME = "test.vm"
IMAGENAME = "centos7-1907"
FLAVOR = "m1.small"
NETWORK = "default_network"
POOL = "external"
KEYPAIR_NAME = "pk"

the_check = []


conn = openstack.connect(cloud=CLOUDNAME)
nova_client = client.Client(2, session=conn)


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
        the_check.append('1')

    except Exception as err:
        the_check.append('0')
#        logging.error("")
        print(err)

    try:
        instance = conn.compute.wait_for_server(instance)
        ip = conn.available_floating_ip()

        conn.compute.add_floating_ip_to_server(
            server=instance.id,
            address=ip.floating_ip_address)

        the_check.append('1')

    except Exception as err:
        the_check.append('0')
#        logging.error("")
        print(err)

    time.sleep(120)  # Sleeping to make sure IP is associated properly

    while True:
        try:
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_socket.connect((ip.floating_ip_address, 22))
            the_check.append('1')
            break
        except Exception as err:
            the_check.append('0')
            print(err)
            break
        finally:
            test_socket.close()
    return instance


def delete_instance(conn, instance):
    """Deletes the VM + floating IP sent to the pool"""

    try:
        conn.compute.delete_server(instance.id, 600)
        the_check.append('1')

    except Exception as err:
        the_check.append('0')
#        logging.error("")
        print(err)


instance = create_instance(conn)
delete_instance(conn, instance)
s = "".join(the_check)
print(s)
