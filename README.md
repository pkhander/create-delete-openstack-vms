# create-delete-instance-check

## What does the script do

This script has four checks so far

1. Can we create a VM succesfully  ? (Add pre-exisitng key pair and security group)
2. Can we assign Floating IP to the VM succesfully ? 
3. Can we SSH in the VM succesfully ?
4. Can we delete the VM succesfully ? 


## Expected output

vm_created:Success, vm_ip_assigned:Success, vm_ssh_connection:Success, vm_deletion:Success

or

vm_created:Success, vm_ip_assigned:Failed, vm_ssh_connection:Failed, vm_deletion:Success  ( + error.log file )