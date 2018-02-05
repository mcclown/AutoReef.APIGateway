import connexion
import six

from swagger.swagger_server.models.color_intensity import ColorIntensity  # noqa: E501
from swagger.swagger_server import util

import requests
import json

light_base_path = "http://192.168.1.101/api"

def get_colors():  # noqa: E501
    """get_colors

    Get the list of valid colors to pass to other colors methods. # noqa: E501


    :rtype: List[str]
    """

    r = requests.get(light_base_path + "/power")

    r_data = r.json()

    if r_data["response_code"] != 0:
        return "Unknown server error", 500

    colors = []

    #Only handling the first device for the moment
    for color in r_data["devices"][0]["normal"]:
        colors.append(color)

    return colors, 200


def get_light_color_intensity():  # noqa: E501
    """get_light_color_intensity

    Get the current status of all colour intensities. # noqa: E501


    :rtype: List[ColorIntensity]
    """
    return 'do some magic!'


def get_light_control():  # noqa: E501
    """get_light_control

    Get the current status of light manual control (enabled/disabled). It is assumed that lights will usually be on a schedule/timer. # noqa: E501


    :rtype: bool
    """

    r = requests.get(light_base_path + '/schedule/enable')

    r_data = r.json()

    if r_data["response_code"] != 0:
        return "Unknown server error", 500

    return not r_data["enable"], 200


def set_light_color_intensity(body):  # noqa: E501
    """set_light_color_intensity

    Update the specified color intensities. # noqa: E501

    :param body: 
    :type body: list | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = [ColorIntensity.from_dict(d) for d in connexion.request.get_json()]  # noqa: E501
    return 'do some magic!'


def set_light_control(enable):  # noqa: E501
    """set_light_control

     # noqa: E501

    :param enable: 
    :type enable: bool

    :rtype: None
    """

    #Invert meaning, since the AquaIllumination light API enables schedules, not manual controls.
    data = {"enable":not enable}

    r = requests.put(light_base_path + "/schedule/enable", data = json.dumps(data) )

    r_data = r.json()

    if r_data['response_code'] != 0:
        return 'Unknown server error', 500
        
    return 'Operation Successful', 200


def update_light_color_intensity(body):  # noqa: E501
    """update_light_color_intensity

    Update a given color by the specified intensity percentage. # noqa: E501

    :param body: 
    :type body: list | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = [ColorIntensity.from_dict(d) for d in connexion.request.get_json()]  # noqa: E501
    return 'do some magic!'
