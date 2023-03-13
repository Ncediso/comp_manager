"""-------------------------
MODULE:
    controllers

DESCRIPTION:
    This package
-------------------------
"""

from .auth_controller import api as auth_ns
from .fa_connect_controller import api as fa_connect_ns
from .permission_controller import api as permission_ns
from .role_controller import api as roles_ns
from .role_permission_controller import api as role_perm_ns
from .user_controller import api as user_ns
from .user_role_controller import api as user_roles_ns
