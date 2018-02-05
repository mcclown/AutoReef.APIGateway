import connexion
import six

from swagger_server.models.color_intensity import ColorIntensity  # noqa: E501
from swagger_server import util


def get_colors():  # noqa: E501
    """get_colors

    Get the list of valid colors to pass to other colors methods. # noqa: E501


    :rtype: List[str]
    """
    return 'do some magic!'


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
    return 'do some magic!'


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
    return 'do some magic!'


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
