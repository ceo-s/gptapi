from fastapi import Request

from .drive import GDriveEventsManager, GDrive
from .db import DBDriveFiles
from .llm.preprocessing import Embedder


async def db_drive_synchronization(event: Request):

    manager = GDriveEventsManager()
    files = await manager.HANDLER.handle_event(headers=event.headers)

    if files is None:
        print("FILES IS NONE =(")
        return

    # await DBDriveFiles().add_files_from_drive(*files.keys())

    # embedder = Embedder(512, 32, 'OverlapOptimizer')
    # for file in files.values():
    #     await embedder.text_to_embeddings(file.content)

    # for file_id, file in files.items():
    #     # if file.fileExtension == "txt":
    #     #     txt_file = file
    #     #     break
    #     print(file)
