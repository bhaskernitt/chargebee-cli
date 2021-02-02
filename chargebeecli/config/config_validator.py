from chargebeecli.constants.error_messages import NO_ACTIVE_PROFILE, ACCOUNT_API_NOT_SET
from chargebeecli.util.printer_util import custom_print


def validate_account_api_key(config):
    if config.has_section("active_profile") is not True:
        custom_print(NO_ACTIVE_PROFILE, err=True)
        exit()
    configured_active_profile = config.get('active_profile', 'primary')

    if config.has_section(configured_active_profile):
        if config.has_section(configured_active_profile):
            if (config.get(configured_active_profile, 'api_key') and config.get(configured_active_profile,
                                                                                'account')) is not None:
                return True
            else:
                custom_print(ACCOUNT_API_NOT_SET, err=True)
                exit()

        else:
            custom_print(ACCOUNT_API_NOT_SET, err=True)
            exit()

    else:
        custom_print(ACCOUNT_API_NOT_SET, err=True)
        exit()

