import requests
from requests.utils import requote_uri
from contextlib import contextmanager
import json, time
from typing import Dict, List, NamedTuple, Optional, Tuple, Union, AnyStr, Literal,TypedDict

class AC2_API():
    session: requests.Session
    api_server: str

    def __init__(self, api_server, username, password):
        data = {
            'username': username,
            'password': password,
            'eulaAccepted': True,
            'verifyCsrfToken': True
        }
        requests.packages.urllib3.disable_warnings()
        self.session =  requests.Session()
        self.api_server = api_server
        responce = self.session.post(url = f'{api_server}/login', json = data, verify=False)
        if responce.status_code != 200:
            raise Exception(f'Error logging: {responce.content}')

    def __enter__(self):
        return self

    def close(self) -> None:
        self.session.post(url = f'{self.api_server}/logout', verify=False)
        self.session.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def devices(self) -> Tuple[int, Union[Dict, List]]:
        '''Returns list of devices managed by current user.'''
        responce = self.session.get(url = f'{self.api_server}/devices', verify=False)
        return responce.status_code, json.loads(responce.content)

    def device(self, mac: Optional[str] = None, device_id: Optional[int] = None) -> Tuple[int, Union[Dict, List]]:
        '''Returns specified device.'''
        assert bool(mac) ^ bool(device_id)
        if mac:
            responce = self.session.get(url = f'{self.api_server}/devices/mac/{requote_uri(mac.upper())}', verify=False)
            return responce.status_code, json.loads(responce.content)
        else:
            responce = self.session.get(url = f'{self.api_server}/devices/{device_id}', verify=False)
            return responce.status_code, json.loads(responce.content)

    def device_alerts(self, mac: Optional[str] = None, device_id: Optional[int] = None) -> Tuple[int, Union[Dict, List]]:
        '''Returns all device specific alerts.'''
        assert bool(mac) ^ bool(device_id)
        if mac:
            status, r = self.device(mac=mac)
            if status != 200: return status, r
            if not isinstance(r, Dict): raise TypeError
            device_id = r['deviceId']
        responce = self.session.get(url = f'{self.api_server}/devices/{device_id}/alerts', verify=False)
        return responce.status_code, json.loads(responce.content)

    def device_events(self, mac: Optional[str] = None, device_id: Optional[int] = None) -> Tuple[int, Union[Dict, List]]:
        '''Returns device specific events for specified time interval.'''
        assert bool(mac) ^ bool(device_id)
        if mac:
            status, r = self.device(mac=mac)
            if status != 200: return status, r
            if not isinstance(r, Dict): raise TypeError('not json returned')
            device_id = r['deviceId']
        responce = self.session.get(url = f'{self.api_server}/devices/{device_id}/events', verify=False)
        return responce.status_code, json.loads(responce.content)
        
    def device_config(self, mac: Optional[str] = None, device_id: Optional[int] = None) -> Tuple[int, Union[AnyStr, Dict, List]]:
        '''Returns device latest configuration backup file.'''
        assert bool(mac) ^ bool(device_id)
        if mac:
            status, r = self.device(mac=mac)
            if status != 200: return status, r
            if not isinstance(r, Dict): raise TypeError
            device_id = r['deviceId']
        responce = self.session.get(url = f'{self.api_server}/devices/{device_id}/config', verify=False)
        return responce.status_code, responce.content

    def device_metrics(self, abstract_metric_request = {'from': 0, 'to': 0, 'scale': 'seconds'},
            mac: Optional[str] = None, device_id: Optional[int] = None) -> Tuple[int, Union[Dict, List]]:
        '''
        Returns specified device metrics.
        FIXME broken
        '''
        assert bool(mac) ^ bool(device_id)
        if mac:
            status, r = self.device(mac=mac)
            if status != 200: return status, r
            if not isinstance(r, Dict): raise TypeError
            device_id = r['deviceId']
        responce = self.session.post(url = f'{self.api_server}/devices/{device_id}/metrics', json=abstract_metric_request, verify=False)
        return responce.status_code, json.loads(responce.content)   
 
