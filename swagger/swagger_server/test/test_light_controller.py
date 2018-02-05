# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.color_intensity import ColorIntensity  # noqa: E501
from swagger_server.test import BaseTestCase


class TestLightController(BaseTestCase):
    """LightController integration test stubs"""

    def test_get_colors(self):
        """Test case for get_colors

        
        """
        response = self.client.open(
            '/AutoReef/AutoReef.ApiGateway/1.0.0/light/colors',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_light_color_intensity(self):
        """Test case for get_light_color_intensity

        
        """
        response = self.client.open(
            '/AutoReef/AutoReef.ApiGateway/1.0.0/light/colorIntensity',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_light_control(self):
        """Test case for get_light_control

        
        """
        response = self.client.open(
            '/AutoReef/AutoReef.ApiGateway/1.0.0/light/manualControl',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_set_light_color_intensity(self):
        """Test case for set_light_color_intensity

        
        """
        body = [ColorIntensity()]
        response = self.client.open(
            '/AutoReef/AutoReef.ApiGateway/1.0.0/light/colorIntensity',
            method='PATCH',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_set_light_control(self):
        """Test case for set_light_control

        
        """
        query_string = [('enable', true)]
        response = self.client.open(
            '/AutoReef/AutoReef.ApiGateway/1.0.0/light/manualControl',
            method='PUT',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_light_color_intensity(self):
        """Test case for update_light_color_intensity

        
        """
        body = [ColorIntensity()]
        response = self.client.open(
            '/AutoReef/AutoReef.ApiGateway/1.0.0/light/colorIntensity/update',
            method='PATCH',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
