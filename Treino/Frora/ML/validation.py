"""Performs requests to the Google Maps Address Validation API."""
from googlemaps import exceptions


_ADDRESSVALIDATION_BASE_URL = "https://addressvalidation.googleapis.com"


def _addressvalidation_extract(response):
    """
    Mimics the exception handling logic in ``client._get_body``, but
    for addressvalidation which uses a different response format.
    """
    body = response.json()
    return body

    # if response.status_code in (200, 404):
    #     return body

    # try:
    #     error = body["error"]["errors"][0]["reason"]
    # except KeyError:
    #     error = None

    # if response.status_code == 403:
    #     raise exceptions._OverQueryLimit(response.status_code, error)
    # else:
    #     raise exceptions.ApiError(response.status_code, error)


def addressvalidation(client, addressLines, regionCode=None , locality=None, enableUspsCass=None):
    """
    The Google Maps Address Validation API returns a verification of an address
    See https://developers.google.com/maps/documentation/address-validation/overview
    request must include parameters below.
    :param addressLines: The address to validate
    :type addressLines: array 
    :param regionCode: (optional) The country code
    :type regionCode: string  
    :param locality: (optional) Restrict to a locality, ie:Mountain View
    :type locality: string
    :param enableUspsCass For the "US" and "PR" regions only, you can optionally enable the Coding Accuracy Support System (CASS) from the United States Postal Service (USPS)
    :type locality: boolean
    """

    params = {
        "address":{
            "addressLines": addressLines
        }
    }

    if regionCode is not None:
        params["address"]["regionCode"] = regionCode

    if locality is not None:
        params["address"]["locality"] = locality

    if enableUspsCass is not False or enableUspsCass is not None:
        params["enableUspsCass"] = enableUspsCass

    return client._request("/v1:validateAddress", {},  # No GET params
                           base_url=_ADDRESSVALIDATION_BASE_URL,
                           extract_body=_addressvalidation_extract,
                           post_json=params)
    