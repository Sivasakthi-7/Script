import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import SubscriptionClient

def list_vms():
    credential = DefaultAzureCredential()
    sub_client = SubscriptionClient(credential)
    for sub in sub_client.subscriptions.list():
        print(f"Subscription: {sub.subscription_id}")
        compute_client = ComputeManagementClient(credential, sub.subscription_id)
        for vm in compute_client.virtual_machines.list_all():
            print(f"  VM Name: {vm.name}")
            print(f"  Location: {vm.location}")
            print(f"  Resource Group: {vm.id.split('/')[4]}")
            nic_ids = [nic.id for nic in vm.network_profile.network_interfaces]
            for nic_id in nic_ids:
                print(f"    NIC ID: {nic_id}")
            print("-" * 40)

if __name__ == "__main__":
    list_vms()