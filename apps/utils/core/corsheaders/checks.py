import re
from collections.abc import Sequence
from numbers import Integral
from urllib.parse import urlparse

from django.conf import settings
from django.core import checks

from apps.utils.core.corsheaders.conf import conf

re_type = type(re.compile(""))


@checks.register
def check_settings(app_configs, **kwargs):
    errors = []

    if not is_sequence(conf.CORS_ALLOW_HEADERS, str):
        errors.append(
            checks.Error(
                "CORS_ALLOW_HEADERS should be a sequence of strings.",
                id="apps.utils.core.corsheaders.E001",
            )
        )

    if not is_sequence(conf.CORS_ALLOW_METHODS, str):
        errors.append(
            checks.Error(
                "CORS_ALLOW_METHODS should be a sequence of strings.",
                id="apps.utils.core.corsheaders.E002",
            )
        )

    if not isinstance(conf.CORS_ALLOW_CREDENTIALS, bool):
        errors.append(
            checks.Error(
                "CORS_ALLOW_CREDENTIALS should be a bool.", id="apps.utils.core.corsheaders.E003"
            )
        )

    if (
        not isinstance(conf.CORS_PREFLIGHT_MAX_AGE, Integral)
        or conf.CORS_PREFLIGHT_MAX_AGE < 0
    ):
        errors.append(
            checks.Error(
                (
                    "CORS_PREFLIGHT_MAX_AGE should be an integer greater than "
                    + "or equal to zero."
                ),
                id="apps.utils.core.corsheaders.E004",
            )
        )

    if not isinstance(conf.CORS_ALLOW_ALL_ORIGINS, bool):
        if hasattr(settings, "CORS_ALLOW_ALL_ORIGINS"):
            allow_all_alias = "CORS_ALLOW_ALL_ORIGINS"
        else:
            allow_all_alias = "CORS_ORIGIN_ALLOW_ALL"
        errors.append(
            checks.Error(
                "{} should be a bool.".format(allow_all_alias), id="apps.utils.core.corsheaders.E005",
            )
        )

    if hasattr(settings, "CORS_ALLOWED_ORIGINS"):
        allowed_origins_alias = "CORS_ALLOWED_ORIGINS"
    else:
        allowed_origins_alias = "CORS_ORIGIN_WHITELIST"

    if not is_sequence(conf.CORS_ALLOWED_ORIGINS, str):
        errors.append(
            checks.Error(
                "{} should be a sequence of strings.".format(allowed_origins_alias),
                id="apps.utils.core.corsheaders.E006",
            )
        )
    else:
        special_origin_values = (
            # From 'security sensitive' contexts
            "null",
            # From files on Chrome on Android
            # https://bugs.chromium.org/p/chromium/issues/detail?id=991107
            "file://",
        )
        for origin in conf.CORS_ALLOWED_ORIGINS:
            if origin in special_origin_values:
                continue
            parsed = urlparse(origin)
            if parsed.scheme == "" or parsed.netloc == "":
                errors.append(
                    checks.Error(
                        "Origin {} in {} is missing scheme or netloc".format(
                            repr(origin), allowed_origins_alias
                        ),
                        id="apps.utils.core.corsheaders.E013",
                        hint=(
                            "Add a scheme (e.g. https://) or netloc (e.g. "
                            + "example.com)."
                        ),
                    )
                )
            else:
                # Only do this check in this case because if the scheme is not
                # provided, netloc ends up in path
                for part in ("path", "params", "query", "fragment"):
                    if getattr(parsed, part) != "":
                        errors.append(
                            checks.Error(
                                "Origin {} in {} should not have {}".format(
                                    repr(origin), allowed_origins_alias, part
                                ),
                                id="apps.utils.core.corsheaders.E014",
                            )
                        )

    if hasattr(settings, "CORS_ALLOWED_ORIGIN_REGEXES"):
        allowed_regexes_alias = "CORS_ALLOWED_ORIGIN_REGEXES"
    else:
        allowed_regexes_alias = "CORS_ORIGIN_REGEX_WHITELIST"
    if not is_sequence(conf.CORS_ALLOWED_ORIGIN_REGEXES, (str, re_type)):
        errors.append(
            checks.Error(
                "{} should be a sequence of strings and/or compiled regexes.".format(
                    allowed_regexes_alias
                ),
                id="apps.utils.core.corsheaders.E007",
            )
        )

    if not is_sequence(conf.CORS_EXPOSE_HEADERS, str):
        errors.append(
            checks.Error(
                "CORS_EXPOSE_HEADERS should be a sequence.", id="apps.utils.core.corsheaders.E008"
            )
        )

    if not isinstance(conf.CORS_URLS_REGEX, (str, re_type)):
        errors.append(
            checks.Error(
                "CORS_URLS_REGEX should be a string or regex.", id="apps.utils.core.corsheaders.E009"
            )
        )

    if not isinstance(conf.CORS_REPLACE_HTTPS_REFERER, bool):
        errors.append(
            checks.Error(
                "CORS_REPLACE_HTTPS_REFERER should be a bool.", id="apps.utils.core.corsheaders.E011"
            )
        )

    if hasattr(settings, "CORS_MODEL"):
        errors.append(
            checks.Error(
                (
                    "The CORS_MODEL setting has been removed - see "
                    + "django-cors-headers' HISTORY."
                ),
                id="apps.utils.core.corsheaders.E012",
            )
        )

    return errors


def is_sequence(thing, type_or_types):
    return isinstance(thing, Sequence) and all(
        isinstance(x, type_or_types) for x in thing
    )
