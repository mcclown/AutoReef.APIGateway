import connexion
import six

from swagger.swagger_server.models.color_intensity import ColorIntensity  # noqa: E501
from swagger.swagger_server.models.color_intensity_change import ColorIntensityChange  # noqa: E501
from swagger.swagger_server import util

from requests import requests, Request
import json
import traceback

light_base_path = "http://192.168.1.101/api"

class Util(object):
    
    @staticmethod
    def response_validation(r_data, r_object=None, response_code = 200):
   
        if r_data["response_code"] != 0:
            return "Unknown server Error", 500
        elif r_data["response_code"] == 0 and r_object != None:
            return r_object, response_code
        else:
            return "Operation Successful", response_code
    
    @staticmethod
    def get_intensity():

        r = requests.get(light_base_path + "/colors")
        
        r_data = None
        r_data = r.json()
    
        if r_data["response_code"] != 0:
            raise Exception("Unable to process /color response")
 
        del r_data["response_code"]

        return r_data

    @staticmethod
    def set_intensity(body):
        
        #req = Request("POST", light_base_path + "/colors", json = body)
        #prepped = req.prepare()
        #print(prepped.body)
        #return 500

        r = requests.post(light_base_path + "/colors", json = body)

        r_data = None
        r_data = r.json()

        if r_data["response_code"] == 0:
            return 200
        else:
            print(r_data)
            return 500

    @staticmethod
    def get_power():

        r = requests.get(light_base_path + "/power")
    
        r_data = None
        power_norm = {}
        power_hd = {}

        r_data = r.json()
    
        if r_data["response_code"] != 0:
            raise Exception("Unable to process /power response")
 
        #Only handling the first device for the moment

        #Get the values for 100%
        for color, value in r_data["devices"][0]["normal"].items():
            power_norm[color] = value
        
        try:
            #Get the values for HD
            for color, value in r_data["devices"][0]["hd"].items():
                power_hd[color] = value
        except Exception:
            #Potentially handle non-HD AI devices? #ToTest
            print("Unable to retrieve HD power values for device")
        
        return power_norm, power_hd


def get_colors():  # noqa: E501
    """get_colors

    Get the list of valid colors to pass to other colors methods. # noqa: E501


    :rtype: List[str]
    """

    r = requests.get(light_base_path + "/power")
    
    r_data = None
    colors = []

    try:
        r_data = r.json()

        #Only handling the first device for the moment
        for color in r_data["devices"][0]["normal"]:
            colors.append(color)

    except Exception as ex:
        print("Error processing get_colors response: ", ex)
    
    return Util.response_validation(r_data, colors)


def get_light_color_intensity():  # noqa: E501
    """get_light_color_intensity

    Get the current status of all colour intensities. # noqa: E501


    :rtype: ColorIntensity
    """
    
    colors = {}

    try:
        
        #Get current LED channel intensities
        intensity = Util.get_intensity()
        
        #Get the power values that represent 100%
        power_norm, power_hd = Util.get_power()
 
        for color, value in intensity.items():
            #Calculate the %power
            
            if value <= 1000:
                colors[color] = round(value/10)
            else:
                #Should never hit this case for a non-HD AI device. #ToTest

                #Calculate max percentage, when using HD
                max_percentage = (power_hd[color] / power_norm[color]) * 100

                #Response from /color: First 1000 is for 0 -> 100%, Second 1000 is for 100% -> Max HD% 
                hd_in_use = (value - 1000) / 1000  

                #Calculate total current percentage
                colors[color] = round(100 + ((max_percentage - 100) * hd_in_use))

    except Exception as ex:
        print("Error processing get_light_color_intensity response: ", traceback.format_exc())
        return "Unknown Server Error", 500
    
    return colors, 200


def get_light_control():  # noqa: E501
    """get_light_control

    Get the current status of light manual control (enabled/disabled). It is assumed that lights will usually be on a schedule/timer. # noqa: E501


    :rtype: bool
    """

    r = requests.get(light_base_path + '/schedule/enable')

    r_data = None 
    
    try:
        r_data = r.json()
    except Exception as ex:
        print("Unable to get light control status: ", ex)

    return Util.response_validation(r_data, not r_data["enable"])


def set_light_color_intensity(body):  # noqa: E501
    """set_light_color_intensity

    Update the specified color intensities. # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    #Validation happens here as well, based on the API specs
    if connexion.request.is_json:
        body = ColorIntensity.from_dict(connexion.request.get_json())  # noqa: E501

    if len(body) < 1:
        return "No color was specified", 400

    try:
        intensity = Util.get_intensity()
        #power_norm, power_hd = Util.get_power()
        
        for color, value in body.items():
            intensity[color] = value * 10

        result = Util.set_intensity(intensity)

        if result != 200:
            return "Unable to set color intensity", result

    except Exception as ex:
        print("Error processing set_light_color_intensity response: ", traceback.format_exc())
        return "Unknown Server Error", 500
 
    return "Operation Successful", 200


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

    r_data = None
    
    try:
        r_data = r.json()
    except Exception as ex:
        print("Unable to set light control: ", ex)

    return Util.response_validation(r_data) 


def update_light_color_intensity(body):  # noqa: E501
    """update_light_color_intensity

    Update a given color by the specified intensity percentage. # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = ColorIntensityChange.from_dict(connexion.request.get_json())  # noqa: E501
    
    if len(body) < 1:
        return "No color was specified", 400

    try:
        intensity = Util.get_intensity()
        #power_norm, power_hd = Util.get_power()
        
        for color, value in body.items():
            temp = intensity[color] + (value * 10)

            #Keep min as 0% and max as 100% (1000 intensity)
            if temp < 0:
                temp = 0
            elif temp > 1000:
                temp = 1000

            intensity[color] = temp

        result = Util.set_intensity(intensity)

        if result != 200:
            return "Unable to update color intensity", result

    except Exception as ex:
        print("Error processing update_light_color_intensity response: ", traceback.format_exc())
        return "Unknown Server Error", 500
 
    return "Operation Successful", 200

