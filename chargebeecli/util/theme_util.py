from chargebeecli.config.Configuration import Configuration
from chargebeecli.processors.themes.available_themes import get_default_theme, get_theme


def get_active_theme():
    section = Configuration.Instance().is_section_exist("active_theme", "theme")
    if section is None:
        return get_default_theme()
    else:
        return get_theme(section)
