from io import BytesIO

import aiofiles


async def upload_file_to_bytes(files):
    try:
        buffer = BytesIO(await files[0].read())

        with open(buffer.getvalue(), 'r') as fp:
            print(fp.readlines())
    except Exception as e:
        print(e)
    # async with aiofiles.open(buffer, 'wb') as stream:
    #     content = await files[0].read()
    #     await stream.write(content)


