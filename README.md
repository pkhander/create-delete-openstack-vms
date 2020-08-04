# create-delete-instance-check

## Pre-reqs

Connection.py file. I used this [link](https://osticket.massopen.cloud/scp/faq.php?id=16).

## What does the script do

This script has three checks so far

1. Create a VM succesfully  ? (Add pre-exisitng key pair and security group)
2. Assign Floating IP succesfully ? 
3. Terminate the VM succesfully ? 

## What does it need

SHH Connection check needs to be added before teminating the VM. 

Key pair and security groups can be created instead of using pre-exisitng ones 

## Expected output

1111

or

[Errno 113] No route to host
1101
