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

"""Managing of ironic-specific keystone domain and users in it."""

# from ironic.common import keystone
from keystoneauth1 import identity
from keystoneauth1 import session
# from keystoneclient import client as kclient
from oslo_config import cfg
from oslo_log import log

from ironic.common.i18n import _
from ironic.conf import CONF

LOG = log.getLogger(__name__)

domain_opts = [
    cfg.StrOpt('ironic_domain_id',
               help=_('ID of ironic-internal domain in keystone')),
    cfg.StrOpt('ironic_domain_admin_name',
               default='ironic_domain_admin',
               help=_('Name of the domain user in the ironic domain')),
    cfg.StrOpt('ironic_domain_admin_password',
               help=_('password for the ironic domain admin user')),
    cfg.StrOpt('ironic_domain_user_role',
               default='ironic_deploy_ramdisk',
               help=_('Default role to assign to a temporary users '
                      'in the ironic domain')),
    cfg.StrOpt('auth_url',
               help=_('Identity service URL')),
]

CONF.register_opts(domain_opts, group='ironic_domain')


IRONIC_DOMAIN_SESSION = None


# NOTE(pas-ha) not using the auth/session loading for now as we need
# a strict KeystoneV3 password auth.
def get_session():
    global IRONIC_DOMAIN_SESSION
    if not IRONIC_DOMAIN_SESSION:
        auth = identity.V3Password(
            auth_url=CONF.ironic_domain.auth_url,
            username=CONF.ironic_domain.ironic_domain_admin_name,
            password=CONF.ironic_domain.ironic_domain_admin_password,
            domain_id=CONF.ironic_domain.ironic_domain_id)
        IRONIC_DOMAIN_SESSION = session.Session(auth=auth)
    return IRONIC_DOMAIN_SESSION


def get_trusted_token(username):
    """Creates domain user and a trust for it."""
    # generate random password
    # create user in ironic domain with this password
    # assign the role to the user
    # create a trust to this user from glance service user, roles?
    # get token with the trust
    pass


def delete_trusted_user(username):
    """Deletes domain user and trust associated with it."""
    # get list of trusts for glance service user
    # find trust that corresponds to username/id
    # delete trust
    # delete the domain user
    pass
