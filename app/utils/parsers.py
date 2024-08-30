from typing import Union,Dict
from datetime import datetime, timedelta

def first_party_caveats_parser(caveats):
    caveats_list_formatted = []
    if "resources" in caveats.keys() and caveats["resources"]:
        surveyCaveat = ""
        for key, value in caveats["resources"].items():
            if value == True:
                surveyCaveat += f"survey_ref_number = {key} OR "
        if surveyCaveat != "":
            surveyCaveat = surveyCaveat[:-4]
        else:
            surveyCaveat = "survey_ref_number = None"
        caveats_list_formatted.append(surveyCaveat)

    if "timeout" in caveats.keys():
        timeout = int(caveats["timeout"])
        expiration_datetime = (datetime.utcnow()+timedelta(seconds=timeout))
        expiration_timestamp = expiration_datetime.isoformat()
        expirationCaveat = f"expiration < {expiration_timestamp}"
        caveats_list_formatted.append(expirationCaveat)
    return caveats_list_formatted
