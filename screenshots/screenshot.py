#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2021 Romain Vigier <contact AT romainvigier.fr>
# SPDX-License-Identifier: GPL-3.0-or-later

"""Run the screenshooter in a headless compositor."""

import os
import subprocess

from typing import Optional


class Widget:
    """Base widget."""

    def __init__(
            self, ui_file: str, image_file: str, css_file: str = None) -> None:
        """Create a new widget.

        Args:
            ui_file (str): Path to the UI file describing the widget.
            image_file (str): Path to the output image file.
            css_file (str, optional): Path to the stylesheet file to load for
                the widget. Defaults to None.
        """
        self.ui_file = ui_file
        self.image_file = image_file
        self.license_file = f"{image_file}.license"
        self.css_file: Optional[str] = css_file


class HelpWidget(Widget):
    """Help widget."""

    def __init__(self, name: str, lang: str, css: bool) -> None:
        """Create a new help widget.

        Args:
            name (str): Name of the widget.
            lang (str): Language of the widget.
            css (bool): If the widget uses a custom stylesheet.
        """
        self.ui_file = os.path.join("screenshots", f"{name}.ui")
        self.image_file = os.path.join("help", lang, "figures", f"{name}.png")
        self.license_file = f"{self.image_file}.license"
        self.css_file = os.path.join("screenshots", f"{name}.css") if css \
            else None


def start_weston() -> subprocess.Popen[bytes]:
    """Start the Weston compositor in headless mode."""
    return subprocess.Popen(["weston", "--backend=headless-backend.so"])


def run_uishooter(
        ui_file: str,
        output: str = None,
        resource_file: str = None,
        resource_path: str = None,
        textdomain: str = None,
        locale: str = None,
        css: str = None,
        dark: bool = False,
        libadwaita: bool = False,) -> int:
    """Shoot the given UI file.

    Args:
        ui_file (str): Path to the UI file.
        output (str, optional): Path to the output image. Defaults to None.
        resource_file (str, optional): Path to a resource file to load.
            Defaults to None.
        resource_path (str, optional): Resource path to load. Defaults to None.
        textdomain (str, optional): Translation textdomain. Defaults to None.
        locale (str, optional): Locale to use. Defaults to None.
        css (str, optional): Path to a CSS file to load. Defaults to None.
        dark (bool, optional): Use dark color scheme. Defaults to False.
        libadwaita (bool, optional): Use libadwaita. Defaults to False.

    Returns:
        int: uishooter exit code
    """
    args = []
    if output:
        args.append(f"--out={output}")
    if resource_file:
        args.append(f"--resource-file={resource_file}")
    if resource_path:
        args.append(f"--resource-path={resource_path}")
    if textdomain:
        args.append(f"--textdomain={textdomain}")
    if locale:
        args.append(f"--locale={locale}")
    if css:
        args.append(f"--css={css}")
    if dark:
        args.append(f"--dark")
    if libadwaita:
        args.append(f"--libadwaita")
    args.append(ui_file)
    uishooter = subprocess.Popen(["uishooter"] + args)
    return uishooter.wait()


def shoot_help() -> None:
    """Shoot widgets for the help pages."""
    with open("help/LINGUAS") as f:
        languages = [lang for lang in f.read().splitlines() if lang[0] != "#"]
    languages.sort()
    for i, lang in enumerate(["C"] + languages):
        for widget in [
                HelpWidget("add-files-button", lang, True),
                HelpWidget("clean-button", lang, False),
                HelpWidget("metadata-example", lang, True)]:
            os.makedirs(os.path.join("help", lang, "figures"), exist_ok=True)
            print(f"[{i}/{len(languages)}|{lang}] Shooting {widget.ui_file}…")
            exit_code = run_uishooter(
                ui_file=widget.ui_file,
                locale=locale_from_lang(lang),
                textdomain="fr.romainvigier.MetadataCleaner",
                resource_path="/fr/romainvigier/MetadataCleaner",
                resource_file="/usr/share/metadata-cleaner/"
                              "fr.romainvigier.MetadataCleaner.gresource",
                css=widget.css_file,
                output=widget.image_file,
                libadwaita=True)
            if exit_code != 0:
                raise RuntimeError(f"Error while shooting {widget.ui_file}.")
            with open(widget.license_file, "w") as f:
                f.writelines([
                    "SPDX-FileCopyrightText: 2021 Romain Vigier "
                    "<contact AT romainvigier.fr>\n",
                    "SPDX-License-Identifier: CC-BY-SA-4.0"
                ])


def locale_from_lang(lang: str) -> str:
    """Get a locale string from a language code.

    Args:
        lang (str): The language code.

    Returns:
        str: The locale string.
    """
    try:
        return {
            "aa": "aa_DJ",
            "af": "af_ZA",
            "ak": "ak_GH",
            "am": "am_ET",
            "an": "an_ES",
            "ar": "ar_TN",
            "as": "as_IN",
            "az": "az_AZ",
            "be": "be_BY",
            "bg": "BG",
            "bho": "bho_IN",
            "bi": "bi_VU",
            "bn": "bn_IN",
            "bo": "bo_CN",
            "br": "br_FR",
            "bs": "bs_BA",
            "ca": "ca_ES",
            "ce": "ce_RU",
            "cs": "cs_CZ",
            "cv": "cv_RU",
            "cy": "cy_GB",
            "da": "da_DK",
            "de": "de_DE",
            "doi": "doi_IN",
            "dv": "dv_MV",
            "dz": "dz_BT",
            "el": "el_GR",
            "en": "en_US",
            "es": "es_ES",
            "et": "et_EE",
            "eu": "eu_ES",
            "fa": "da_IR",
            "ff": "ff_SN",
            "fi": "fi_FI",
            "fil": "fil_PH",
            "fo": "fo_FO",
            "fr": "fr_FR",
            "fy": "fy_DE",
            "ga": "ga_IE",
            "gd": "gd_GB",
            "gl": "gl_ES",
            "gu": "gu_IN",
            "gv": "gv_GB",
            "ha": "ha_NG",
            "he": "he_IL",
            "hi": "hi_IN",
            "hr": "hr_HR",
            "ht": "ht_HT",
            "hu": "hu_HU",
            "hy": "hy_AM",
            "ia": "ia_FR",
            "id": "id_ID",
            "ig": "ig_NG",
            "ik": "ik_CA",
            "is": "is_IS",
            "it": "it_IT",
            "iu": "iu_CA",
            "ja": "ja_JP",
            "kab": "kab_DZ",
            "ka": "ka_GE",
            "kk": "kk_KZ",
            "kl": "kl_GL",
            "km": "km_KH",
            "kn": "kn_IN",
            "ko": "ko_KR",
            "ks": "ks_IN",
            "ku": "ku_TR",
            "kw": "kw_GB",
            "ky": "ky_KG",
            "lb": "lb_LU",
            "lg": "lg_UG",
            "li": "li_BE",
            "ln": "ln_CS",
            "lo": "lo_LA",
            "lt": "lt_LT",
            "lv": "lv_LV",
            "mag": "mag_IN",
            "mai": "mai_IN",
            "mg": "mg_MG",
            "mi": "mi_NZ",
            "mk": "mk_MK",
            "ml": "ml_IN",
            "mni": "mni_IN",
            "mn": "mn_MN",
            "mr": "mr_IN",
            "ms": "ms_MY",
            "mt": "mt_MT",
            "my": "my_MM",
            "nb": "nb_NO",
            "ne": "ne_NP",
            "nl": "nl_NL",
            "nn": "nn_NO",
            "nr": "nr_ZA",
            "nso": "nso_ZA",
            "oc": "oc_FR",
            "om": "om_ET",
            "or": "or_IN",
            "os": "os_RU",
            "pa": "pa_IN",
            "pl": "pl_PL",
            "pt": "pt_PT",
            "raj": "raj_IN",
            "ro": "ro_RO",
            "ru": "ru_RU",
            "rw": "rw_RW",
            "sa": "sa_IN",
            "sc": "sc_IT",
            "sd": "sd_IN",
            "se": "se_NO",
            "shn": "shn_MM",
            "sid": "sid_ET",
            "si": "si_LK",
            "sk": "sk_SK",
            "sl": "sl_SI",
            "sm": "sm_WS",
            "so": "so_SO",
            "sq": "sq_AL",
            "sr": "sr_RS",
            "ss": "ss_ZA",
            "st": "st_ZA",
            "sv": "sv_SE",
            "sw": "sw_TZ",
            "ta": "ta_IN",
            "te": "te_IN",
            "tg": "tg_TJ",
            "th": "th_TH",
            "ti": "ti_ER",
            "tk": "tk_TM",
            "tl": "tl_PH",
            "tn": "tn_ZA",
            "to": "to_TO",
            "tr": "tr_TR",
            "ts": "ts_ZA",
            "tt": "tt_RU",
            "ug": "ug_CN",
            "uk": "uk_UA",
            "ur": "ur_PK",
            "uz": "uz_UZ",
            "ve": "ve_ZA",
            "vi": "vi_VN",
            "wa": "wa_BE",
            "wo": "wo_SN",
            "xh": "xh_ZA",
            "yi": "yi_US",
            "yo": "yo_NG",
            "zh": "zh_CN",
            "zh_Hant": "zh_CN",
            "zu": "zu_ZA",
        }[lang]
    except KeyError:
        return lang


if __name__ == "__main__":
    weston = None
    try:
        weston = start_weston()
        shoot_help()
    finally:
        if weston:
            weston.terminate()
