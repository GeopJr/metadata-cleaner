<!--
SPDX-FileCopyrightText: 2020 Romain Vigier <contact AT romainvigier.fr>
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# Metadata Cleaner

![](./data/icons/hicolor/scalable/apps/fr.romainvigier.MetadataCleaner.svg)

Metadata within a file can tell a lot about you. Cameras record data about when a picture was taken and what camera was used. Office applications automatically add author and company information to documents and spreadsheets. Maybe you don't want to disclose those informations.

This tool allows you to view metadata in your files and to get rid of them, as much as possible.

Under the hood, it relies on [mat2](https://0xacab.org/jvoisin/mat2) to parse and remove the metadata.

---

[[_TOC_]]

---

## Screenshots

![Welcome screen](./data/screenshots/1.png)
![Metadata details window](./data/screenshots/2.png)
![Cleaned files](./data/screenshots/3.png)

## Installing

Metadata Cleaner is available as a Flatpak on Flathub:

<a href="https://flathub.org/apps/details/fr.romainvigier.MetadataCleaner"><img src="https://flathub.org/assets/badges/flathub-badge-en.png" alt="Download on Flathub" width="240"></a>

## Building from source

Dependencies:

- `gtk+-3.0` >= 3.24
- `libhandy-1`
- `pygobject-3.0`
- `python3`
- Python 3 `libmat2` module and [its dependencies](https://0xacab.org/jvoisin/mat2#requirements)

Metadata Cleaner uses the meson build system:

```sh
meson builddir
meson install -C builddir
```

Flatpak building is also available and requires the GNOME 3.38 platform and SDK:

```sh
flatpak-builder --force-clean --user --install builddir data/fr.romainvigier.MetadataCleaner.yaml
```

## Contributing

See [`CONTRIBUTING.md`](./CONTRIBUTING.md).
