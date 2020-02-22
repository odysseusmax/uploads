import asyncio

import aiohttp

upload_url = "http://195.154.232.19:7000/upload_request"      #   Inspect the upload page and grab it (may change in future).
auth_mail = ""                                                #   Email with which you signed up.
auth_password =                                               #   Inspect the upload page and grab it.

async def main():
  async with aiohttp.ClientSession() as session:
    file_to_upload = ''                                       #   Path to the file.
    data = {'file' : open(file_to_upload, 'rb'),
      'folder_id': '0',                                       #   Folder to which uploads go.
      'auth_mail': auth_mail,
      'auth_password': auth_password,
      'domain': 'upindia.mobi',
      'ajax': 'yes'
    }
    r = await session.post(upload_url, data=data)
    print(await r.text())                                      #   Response will be a html page with json formated data.

asyncio.run(main())
