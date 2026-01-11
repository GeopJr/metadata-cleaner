<p align="center">
  <img alt="A rectangle with a fingerprint on it being wiped using a sponge" width="160" src="./data/icons/dev.geopjr.MetadataCleaner.svg">
</p>
<h1 align="center">Metadata Cleaner</h1>
<h3 align="center">View and clean metadata in files</h3>
<p align="center">
  <br />
    <a href="./CODE_OF_CONDUCT.md"><img src="https://img.shields.io/badge/Code%20of%20Conduct-GNOME-f5c211.svg?style=for-the-badge&labelColor=f9f06b" alt="GNOME Code of Conduct" /></a>
    <a href="./LICENSE"><img src="https://img.shields.io/badge/LICENSE-GPL--3.0-f5c211.svg?style=for-the-badge&labelColor=f9f06b" alt="License GPL-3.0" /></a>
    <a href='https://stopthemingmy.app'><img width='193.455' alt='Please do not theme this app' src='https://stopthemingmy.app/badge.svg'/></a>
</p>

<p align="center">
    <img alt="Screenshot of the Metadata Cleaner app in light mobile. A bunch of files are ready to be cleaned. gnome-story.webp is open and has 4 metadata visible in a side panel." src="./data/screenshots/screenshot-1.png">
</p>

<p align="center">Metadata within a file can tell a lot about you. Cameras record data about when and where a picture was taken and which camera was used. Office applications automatically add author and company information to documents and spreadsheets. This is sensitive information and you may not want to disclose it. Metadata Cleaner allows you to view metadata in your files and to get rid of it, as much as possible.</p>

# Install

## Official

### Release

<a href="https://flathub.org/apps/details/dev.geopjr.MetadataCleaner" rel="noreferrer noopener" target="_blank"><img loading="lazy" draggable="false" width='240' alt='Download on Flathub' src='https://flathub.org/api/badge?svg&locale=en' /></a>

## From Source

<details>
<summary>Dependencies</summary>

Package Name | Required
:--- | ---:
meson | ✅
python3 | ✅
libadwaita-1.0-dev | ✅
mat2 | ✅

</details>

### Makefile

```
$ make
$ make install
```

### GNOME Builder

- Clone
- Open in GNOME Builder

# Acknowledgements

- Metadata cleaning is being done using [mat2](https://github.com/jvoisin/mat2)
- This is a fork of [rmnvgr/metadata-cleaner](https://gitlab.com/rmnvgr/metadata-cleaner)
- The original artwork, translations, `metadata-cleaner.doap` are released under the terms of the [Creative Commons Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/).

# Sponsors

<div align="center">

[![GeopJr Sponsors](https://cdn.jsdelivr.net/gh/GeopJr/GeopJr@main/sponsors.svg)](https://github.com/sponsors/GeopJr)

</div>

[![Translation status](https://translate.codeberg.org/widgets/metadata-cleaner/-/metadata-cleaner/287x66-white.png)](https://translate.codeberg.org/engage/metadata-cleaner)

# Contributing

1. Read the [Code of Conduct](./CODE_OF_CONDUCT.md)
2. Fork it ( https://codeberg.org/GeopJr/metadata-cleaner/fork )
3. Create your feature branch (git checkout -b my-new-feature)
4. Commit your changes (git commit -am 'Add some feature')
5. Push to the branch (git push origin my-new-feature)
6. Create a new Pull Request
