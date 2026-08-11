# checkuser.py file is part of spman
#
# spman - Slackware package manager
# Home page: https://github.com/MyRequiem/spman
#
# Copyright (c) 2018 Vladimir MyRequiem Astrakhan, Russia
# <mrvladislavovich@gmail.com>
# All rights reserved
# See LICENSE for details.

"""Check superuser privileges."""

import os

ERROR_NOT_ROOT = "spman can only be run as root."

def check_root_user() -> None:
    """Verify that the script is executed with root privileges.

    Raises:
        PermissionError: If the current effective user ID is not 0 (root).

    """
    if os.getuid() != 0:
        raise PermissionError(ERROR_NOT_ROOT)
