import json

__metaclass__ = type

DOCUMENTATION = '''
---
module: hv_sds_block_CHAP_user
short_description: Manage Hitachi sds block storage system CHAP users.
description:
  - This module allows for the creation, deletion and updation of CHAP users.
  - It supports various CHAP user operations based on the specified task level.
version_added: '3.0.0'
author:
  - Hitachi Vantara, LTD. VERSION 3.0.0
requirements:
options:
  state:
    description: The level of the CHAP user task. Choices are 'present', 'absent'.
    type: str
    required: true
  connection_info:
    description: Information required to establish a connection to the storage system.
    required: true
    type: dict
    suboptions:
      address:
        description: IP address or hostname of the storage system.
        type: str
        required: true
      username:
        description: Username for authentication.
        type: str
        required: true
      password:
        description: Password for authentication.
        type: str
        required: true
      connection_type:
        description: Type of connection to the storage system.
        type: str
        required: true
        choices: ['direct', 'gateway']
  spec:
    description: Specification for the CHAP user task.
    type: dict
    required: true
    suboptions:
      id:
        description: ID of the CHAP user.
        type: str
        required: false
      target_chap_user_name:
        description: Target CHAP user name.
        type: str
        required: false
      target_chap_secret:
        description: Target CHAP user secret.
        type: str
        required: false
      initiator_chap_user_name:
        description: Initiator CHAP user name.
        type: str
        required: false
      initiator_chap_secret:
        description: Initiator CHAP user secret.
        type: str
        required: false
'''

EXAMPLES = '''
- name: Create a CHAP user
  hv_sds_block_CHAP_user:
    state: present
    connection_info:
      address: vssb.company.com
      username: "admin"
      password: "password"
      connection_type: "direct"
    spec:
      target_chap_user_name: "chapuser2"
      target_chap_user_secret: "chapuser2_secret"
      initiator_chap_user_name: "chapuser1"
      initiator_chap_secret: "chapuser1_secret"

- name: Delete a CHAP user
  hv_sds_block_CHAP_user:
    state: present
    connection_info:
      address: vssb.company.com
      username: "admin"
      password: "password"
      connection_type: "direct"
    spec:
      id: "464e1fd1-9892-4134-866c-6964ce786676"

- name: Update chap user name
  hv_sds_block_CHAP_user:
    state:
    connection_info:
      address: vssb.company.com
      username: "admin"
      password: "password"
      connection_type: "direct"
    spec:
      id: "464e1fd1-9892-4134-866c-6964ce786676"
      target_chap_user_name: "newchapuser2"

- name: Update chap user secret
  hv_sds_block_CHAP_user:
    state:
    connection_info:
      address: vssb.company.com
      api_token: "api_token_value"
      connection_type: "direct"
    spec:
      id: "464e1fd1-9892-4134-866c-6964ce786676"
      target_chap_user_name: "chapuser2"
      target_chap_user_secret: "chapuser2_new_secret"
'''

RETURN = '''
data:
  description: The CHAP user information.
  returned: always
  type: dict
  elements: dict
  sample:
    {
      "id": "464e1fd1-9892-4134-866c-6964ce786676",
      "initiator_chap_user_name": "chapuser1",
      "target_chap_user_name": "newchapuser2"
    }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.hv_constants import (
    StateValue,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.reconciler.sdsb_chap_users import (
    SDSBChapUserReconciler,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.reconciler.sdsb_properties_extractor import (
    ChapUserPropertiesExtractor,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.hv_log import Log
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.sdsb_utils import (
    SDSBChapUserArguments,
    SDSBParametersManager,
)

logger = Log()


class SDSBChapUserManager:
    def __init__(self):

        self.argument_spec = SDSBChapUserArguments().chap_user()
        logger.writeDebug(
            f"MOD:hv_sds_block_CHAP_user:argument_spec= {self.argument_spec}"
        )
        self.module = AnsibleModule(
            argument_spec=self.argument_spec,
            supports_check_mode=True,
            # can be added mandotary , optional mandatory arguments
        )

        parameter_manager = SDSBParametersManager(self.module.params)
        self.state = parameter_manager.get_state()
        self.connection_info = parameter_manager.get_connection_info()
        # logger.writeDebug(f"MOD:hv_sds_block_CHAP_user_facts:argument_spec= {self.connection_info}")
        self.spec = parameter_manager.get_chap_user_spec()
        # logger.writeDebug(f"MOD:hv_sds_block_CHAP_user_facts:spec= {self.spec}")

    def apply(self):
        chap_users = None
        chap_user_data_extracted = None

        logger.writeInfo(f"{self.connection_info.connection_type} connection type")
        try:
            sdsb_reconciler = SDSBChapUserReconciler(self.connection_info)
            chap_users = sdsb_reconciler.reconcile_chap_user(self.state, self.spec)

            logger.writeDebug(
                f"MOD:hv_sds_block_CHAP_user_facts:chap_users= {chap_users}"
            )
            if self.state.lower() == StateValue.ABSENT:
                chap_user_data_extracted = chap_users
            else:
                output_dict = chap_users.to_dict()
                chap_user_data_extracted = ChapUserPropertiesExtractor().extract_dict(
                    output_dict
                )
        except Exception as e:
            self.module.fail_json(msg=str(e))

        response = {"changed": self.connection_info.changed, "data": chap_user_data_extracted}
        self.module.exit_json(**response)


def main(module=None):
    obj_store = SDSBChapUserManager()
    obj_store.apply()


if __name__ == "__main__":
    main()
