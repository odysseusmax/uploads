import asyncio
import errno
import re
import os

import aiohttp


class Upindia:
    
    def __init__(self, mail, password, domain='upindia.mobi'):
        """
            Parameters:
                mail : Mail address with which you signed up.
                password : Your password.
                domain : any of 'upindia.mobi', 'uploadfile.cc', or 'upload.mobi'. Defaults to 'upindia.mobi'.
        """
        
        self._mail = mail
        self._password = password
        if domain not in ['upindia.mobi', 'uploadfile.cc', 'upload.mobi']:
            raise ValueError(f'Unsupported domain! {domain}')
        self._domain = "https://" + domain
        
        self._session = aiohttp.ClientSession()
        self.is_logged_in = False
    
    async def _login(self):
        login_action = self._domain + '/login?run'
        login_payload = {
            'mail':self._mail,
            'password':self._password
        }
        r = await self._session.post(login_action, data=login_payload)
        html = await r.text()
        error = re.findall(r'class="error"', html)
        if error:
            raise ValueError('Email or password is incorrect')
        self.is_logged_in = True
    
    
    async def upload_file(self, file_path):
        """
            Function uploads the provided file.
            
            Parameters:
                file_path : path to the file.
            
            Returns:
                Returns download link upon successfull upload.
        """
        
        if not os.path.isfile(file_path):
            # https://stackoverflow.com/questions/36077266/how-do-i-raise-a-filenotfounderror-properly
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_path)
        
        if not self.is_logged_in:
            await self._login()
        
        upload_page = self._domain + '/upload_multi'
        upload_payload = {}
        r = await self._session.get(upload_page)
        html = await r.text()
        upload_url = re.findall(
            r'action="([^"]+)"',
            html
        )[0]
        upload_params = re.findall(
            r'name="([^"]+)"\s*value="([^"]+)"',
            html
        )
        for name, value in upload_params:
            upload_payload[name] = value
        upload_payload['file'] = open(file_path, 'rb')
        r = await self._session.post(upload_url, data=upload_payload)
        upload_response = await r.json(content_type=None)
        if 'success' in upload_response['type']:
            info = upload_response['info']
            file_id = info['file_id']
            file_code = info['file_code']
            return self._domain + f"/{file_id}/{file_code}"
