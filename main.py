"""Encapsulate interaction between Grist and the vSphere API."""

# from grist_api import GristDocAPI
import pprint
import os
import requests
from dotenv import load_dotenv
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim

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

def get_vm_tags(vsphereclient, vm_id):
    """Get tags attached to a VM."""
    response = vsphereclient.post(
        "/api/cis/tagging/tag-association?action=list-attached-tags",
        json={"object_id": {"id": vm_id, "type": "VirtualMachine"}}
    )
    response.raise_for_status()
    tag_ids = response.json()

    tags = []
    for tag_id in tag_ids:
        tag = vsphereclient.get(f"/api/cis/tagging/tag/{tag_id}").json()
        category = vsphereclient.get(f"/api/cis/tagging/category/{tag['category_id']}").json()
        tags.append({
            "category": category["name"],
            "tag": tag["name"]
        })
    return tags

def get_custom_attributes(host, username, password, vm_id):
    """Get custom attributes for a VM via SOAP API."""
    si = SmartConnect(host=host, user=username, pwd=password)
    content = si.RetrieveContent()

    # Build a lookup of custom field key -> name
    field_names = {f.key: f.name for f in content.customFieldsManager.field}

    # Find the VM
    #searcher = content.searchIndex
    vm = content.searchIndex.FindByUuid(None, vm_id, True)

    # If FindByUuid doesn't work, search by inventory path or iterate
    if vm is None:
        container = content.viewManager.CreateContainerView(
            content.rootFolder, [vim.VirtualMachine], True
        )
        for v in container.view:
            if v._moId == vm_id:  # pylint: disable=protected-access
                vm = v
                break
        container.Destroy()

    if vm is None:
        raise ValueError(f"VM {vm_id} not found")

    attrs = {}
    for value in vm.customValue:
        attrs[field_names[value.key]] = value.value

    Disconnect(si)
    return attrs

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
    print("\n\nSpecifically the nic info,")
    pprint.pprint(vm_dict['vm-932832']['nics'])
    print("\n\n and the tags for that machine?")
    pprint.pprint(get_vm_tags(client, 'vm-932832'))
    print("\n\n and the Version,")
    print(client.get("/api/appliance/system/version").json())
    print("\n\n Custom atts?")
    attys = get_custom_attributes("vc-oit02.oit.umn.edu",
                                  os.environ["VSPHERE_USER"],
                                  os.environ["VSPHERE_PASS"],
                                  'vm-932832')
    pprint.pprint(attys)

if __name__ == "__main__":
    main()
