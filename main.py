"""Encapsulate interaction between Grist and the vSphere API."""

# from grist_api import GristDocAPI
import pprint
import os
import requests
from dotenv import load_dotenv

load_dotenv()

GRIST_BASE_URL = "https://grist.cla.umn.edu"
VSPHERE_BASE_URL = "https://vc-oit02.oit.umn.edu"

class VSphereClient:
    """Auth and provide a client for vSphere."""
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.verify = True

        # Sign in is part of the cis API.
        response = self.session.post(
            f"{self.base_url}/api/session",
            auth=(username, password),
        )
        response.raise_for_status()

        self.session.headers["vmware-api-session-id"] = response.json()

    def get(self, path, **kwargs):
        """GET method for vSphere client."""
        return self.session.get(f"{self.base_url}{path}", **kwargs)

    def post(self, path, **kwargs):
        """POST method for vSphere client."""
        return self.session.post(f"{self.base_url}{path}", **kwargs)


def get_vm_data(vsphereclient, vm_name):
    """Get the info for a VM."""
    path = f"/api/vcenter/vm/{vm_name}"

    response = vsphereclient.get(path)
    response.raise_for_status()
    return response.json()

def build_vm_dict(vsphereclient, vm_list):
    """Create a dict with the vm-name as the key with the info as values."""
    vm_dict = {}

    for vm in vm_list:
        vm_dict[vm['vm']] = {}
        vm_info = get_vm_data(vsphereclient, vm['vm'])
        vm_dict[vm['vm']] = vm_info

    return vm_dict

def main():
    """Run the vSphere calls."""
    client = VSphereClient(
        VSPHERE_BASE_URL,
        os.environ["VSPHERE_USER"],
        os.environ["VSPHERE_PASS"],
    )
    vms = client.get("/api/vcenter/vm").json()
    vm_dict = build_vm_dict(client, vms)

    pprint.pprint(vm_dict['vm-932832'])
    pprint.pprint(vm_dict['vm-932832']['nics'])


if __name__ == "__main__":
    main()
