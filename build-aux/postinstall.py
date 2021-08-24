#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2020, 2021 Romain Vigier <contact AT romainvigier.fr>
# SPDX-License-Identifier: GPL-3.0-or-later

"""Post-install task."""

import os
import subprocess

prefix = os.environ.get("MESON_INSTALL_PREFIX", "/usr/local")
datadir = os.path.join(prefix, "share")

if "DESTDIR" not in os.environ:
    print("Updating desktop database...")
    desktop_database_dir = os.path.join(datadir, "applications")
    subprocess.call(["update-desktop-database", "-q", desktop_database_dir])
