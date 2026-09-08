# vSphere Grist Tool

To use this you'll need to create a .env file with the following,
```
VSPHERE_USER=<username>
VSPHERE_PASS=<password>
```

## Usage in a Python `venv`
Pull down the repo,

```
git@github.com:hahnx117/vsphere_grist.git
```

Once inside the repo, create a Python virtual environment,

```
python3 -m venv .
```

Now install the `pip` requirements,

```
python3 -m pip install -r requirements.txt
```

To run (and see sample output right now),

```
python main.py
```

## Sample output
```
$ python main.py 
{'boot': {'delay': 0,
          'enter_setup_mode': False,
          'retry': False,
          'retry_delay': 10000,
          'type': 'BIOS'},
 'boot_devices': [],
 'cdroms': {'3000': {'allow_guest_control': True,
                     'backing': {'device_access_type': 'EMULATION',
                                 'type': 'CLIENT_DEVICE'},
                     'ide': {'master': True, 'primary': True},
                     'label': 'CD/DVD drive 1',
                     'start_connected': False,
                     'state': 'NOT_CONNECTED',
                     'type': 'IDE'}},
 'cpu': {'cores_per_socket': 1,
         'count': 2,
         'hot_add_enabled': False,
         'hot_remove_enabled': False},
 'disks': {'2000': {'backing': {'type': 'VMDK_FILE',
                                'vmdk_file': '[Hosting-01_022_122] '
                                             'cla-schraterlab/cla-schraterlab.vmdk'},
                    'capacity': 68719476736,
                    'label': 'Hard disk 1',
                    'scsi': {'bus': 0, 'unit': 0},
                    'type': 'SCSI'}},
 'floppies': {},
 'guest_OS': 'CENTOS_64',
 'hardware': {'upgrade_policy': 'NEVER',
              'upgrade_status': 'NONE',
              'version': 'VMX_13'},
 'identity': {'bios_uuid': '4227c58f-24e5-5ab5-8830-d825aade11b3',
              'instance_uuid': '50274680-d977-c63d-42a4-20b9e0d5df81',
              'name': 'cla-schraterlab'},
 'instant_clone_frozen': False,
 'memory': {'hot_add_enabled': False,
            'hot_add_increment_size_MiB': 0,
            'hot_add_limit_MiB': 4096,
            'size_MiB': 4096},
 'name': 'cla-schraterlab',
 'nics': {'4000': {'allow_guest_control': False,
                   'backing': {'connection_cookie': 1134348611,
                               'distributed_port': '2660',
                               'distributed_switch_uuid': '50 27 10 b0 e3 f2 '
                                                          'c5 bb-d8 ce d0 85 '
                                                          '57 24 88 6e',
                               'network': 'dvportgroup-3427076',
                               'type': 'DISTRIBUTED_PORTGROUP'},
                   'label': 'Network adapter 1',
                   'mac_address': '00:50:56:a7:73:fd',
                   'mac_type': 'ASSIGNED',
                   'pci_slot_number': 160,
                   'start_connected': True,
                   'state': 'CONNECTED',
                   'type': 'VMXNET3',
                   'upt_compatibility_enabled': True,
                   'upt_v2_compatibility_enabled': False,
                   'wake_on_lan_enabled': True}},
 'nvme_adapters': {},
 'parallel_ports': {},
 'power_state': 'POWERED_ON',
 'sata_adapters': {},
 'scsi_adapters': {'1000': {'label': 'SCSI controller 0',
                            'pci_slot_number': 16,
                            'scsi': {'bus': 0, 'unit': 7},
                            'sharing': 'NONE',
                            'type': 'LSILOGIC'}},
 'serial_ports': {}}


Specifically the nic info,
{'4000': {'allow_guest_control': False,
          'backing': {'connection_cookie': 1134348611,
                      'distributed_port': '2660',
                      'distributed_switch_uuid': '50 27 10 b0 e3 f2 c5 bb-d8 '
                                                 'ce d0 85 57 24 88 6e',
                      'network': 'dvportgroup-3427076',
                      'type': 'DISTRIBUTED_PORTGROUP'},
          'label': 'Network adapter 1',
          'mac_address': '00:50:56:a7:73:fd',
          'mac_type': 'ASSIGNED',
          'pci_slot_number': 160,
          'start_connected': True,
          'state': 'CONNECTED',
          'type': 'VMXNET3',
          'upt_compatibility_enabled': True,
          'upt_v2_compatibility_enabled': False,
          'wake_on_lan_enabled': True}}
```