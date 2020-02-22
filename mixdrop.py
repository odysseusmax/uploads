import asyncio

import aiohttp

upload_url = "https://ul.mixdrop.co/api"
email = ""                                          #   Sign in and grab from https://mixdrop.co/api
key = ""                                            #   Sign in and grab from https://mixdrop.co/api

async def main():
  async with aiohttp.ClientSession() as session:
    file_to_upload = ""                             #   Path to file.
    data = {'file': open(file_to_upload, 'rb'),
      'email': email,
      'key': key
    }
    r = await session.post(upload_url, data=data)
    print(await r.json())

asyncio.run(main())
