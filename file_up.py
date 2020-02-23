import asyncio

import aiohttp

upload_url = "https://f4.file-upload.download/cgi-bin/upload.cgi?upload_type=file&utype=anon"


async def main():
  async with aiohttp.ClientSession() as session:
    data = aiohttp.FormData()
    data.add_field('file',
      open('@Jpg2PdfBot.PDF', 'rb'),
      filename = '@Jpg2PdfBot.PDF'
    )
    r = await session.post(upload_url, data=data)
    print(r.status)
    print(await r.text())

asyncio.run(main())
