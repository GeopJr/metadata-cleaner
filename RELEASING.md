<!--
SPDX-FileCopyrightText: Metadata Cleaner contributors
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# Releasing

Release checklist:

- Bump version number in [`meson.build`](./meson.build)
- Add entry in [`CHANGELOG.md`](./CHANGELOG.md)
- Add release notes to [the metainfo file](./application/data/fr.romainvigier.MetadataCleaner.metainfo.xml)

To make a release, create a new tag. The CI will automatically add release notes.
