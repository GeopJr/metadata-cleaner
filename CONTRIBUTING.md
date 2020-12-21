<!--
SPDX-FileCopyrightText: 2020 Romain Vigier <contact AT romainvigier.fr>
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# Contributing

---

[[_TOC_]]

---

## Code

Metadata Cleaner is written in Python 3. It follows the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide, the [PEP 257](https://www.python.org/dev/peps/pep-0257/) doctring conventions and the [PEP 484](https://www.python.org/dev/peps/pep-0484/) type hints.

Open a new merge request with your changes, the CI will automatically check your code.

## Translations

If you want to add a new language, add its code in a new line in the [`./po/LINGUAS`](./po/LINGUAS) file.

Run these commands to update the `po` files:

```sh
meson builddir
cd builddir
meson compile fr.romainvigier.MetadataCleaner-pot
meson compile fr.romainvigier.MetadataCleaner-update-po
```

Edit your language file in the [`./po/`](./po) directory.

## Copyright notices

When you change or add files, add your copyright notice to the top of the file, or in a separate file (named `original-file.ext.license`), following the [SPDX specification](https://spdx.dev/).

The CI will warn you if you add a file without specifying its license.

## Commit messages

If you make a merge request with only one commit, specify in its message which part of the program you worked on, then what your changes do. If you make a merge request with multiple commits, they will be squashed into a single commit: you can change the commit message when making the merge request.

Message examples:

```
Status indicator: Add details about the current operation
```
or
```
Translation: Update French
```

## Support

I've written this application for the benefit of everyone, if you want to help me in return, please consider [supporting me on Liberapay](https://liberapay.com/rmnvgr/)!
