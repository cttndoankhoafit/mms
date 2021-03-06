#!/usr/bin/env python
"""
Command-line utility for administrative tasks.
Sửa lần cuối bởi: Thiên Tứ
"""

import os
import sys

if __name__ == "__main__":
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "mms.settings"
    )

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
