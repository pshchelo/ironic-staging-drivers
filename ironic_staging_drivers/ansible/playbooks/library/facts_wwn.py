#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

try:
    import pyudev
    HAS_PYUDEV = True
except ImportError:
    HAS_PYUDEV = False


COLLECT_INFO = (('wwn', 'WWN'), ('serial', 'SERIAL_SHORT'),
                ('wwn_with_extension', 'WWN_WITH_EXTENSION'),
                ('wwn_vendor_extension', 'WWN_VENDOR_EXTENSION'))


def get_devices_wwn(devices):

    if not HAS_PYUDEV:
        LOG.warning('Can not collect "wwn", "wwn_with_extension", '
                    '"wwn_vendor_extension" and "serial" when using '
                    'root device hints because there\'s no UDEV python '
                    'binds installed')
        return

    dev_dict = {}
    context = pyudev.Context()
    for device in devices:
        name = '/dev/' + device
        try:
            udev = pyudev.Device.from_device_file(context, name)
        except (ValueError, EnvironmentError, pyudev.DeviceNotFoundError) as e:
            LOG.warning('Device %(dev)s is inaccessible, skipping... '
                        'Error: %(error)s', {'dev': name, 'error': e})
            continue

        dev_dict[device] = {}
        for key, udev_key in COLLECT_INFO:
            dev_dict[device][key] = udev.get('ID_%s' % udev_key)

    return {"ansible_facts": {"devices_wwn": dev_dict}}


def main():
    module = AnsibleModule(
        argument_spec=dict(
            devices=dict(required=True, type='list'),
        ),
        supports_check_mode=True,
    )

    devices = module.params['devices']
    data = get_devices_wwn(devices)
    module.exit_json(**data)


from ansible.module_utils.basic import *  # noqa
if __name__ == '__main__':
    main()
