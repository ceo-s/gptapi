from fastapi import Request
from typing import Sequence

from .drive import GDriveEventsManager, GDrive
from .db import DBDriveFiles, DBDocuments
from .llm.preprocessing import Embedder
import db.interfaces as I


async def db_drive_synchronization(event: Request):

    manager = GDriveEventsManager()
    files_mapping = await manager.HANDLER.handle_event(headers=event.headers)

    if not files_mapping:
        print("FILES IS NONE =(")
        return
    print(files_mapping)

    drive_files_manager = DBDriveFiles()
    existing_files = await drive_files_manager.list_files(tuple(files_mapping.keys()))

    # File ids to exclude from re-embedding
    excluded = []

    for fileid_content_tuple in existing_files:
        if files_mapping[fileid_content_tuple[0]].content == fileid_content_tuple[1]:
            excluded.append(fileid_content_tuple[0])

    await drive_files_manager.add_files_from_drive(tuple(files_mapping.values()))
    await embed_into_chunked_documents(files_mapping.values(), excluded)


async def embed_into_chunked_documents(files: Sequence[I.File], excluded: Sequence[str]):

    embedder = Embedder(512, 32, 'OverlapOptimizer')
    documents_manager = DBDocuments()

    for file in files:
        if file.trashed:
            await documents_manager.delete_documents(file.id)

        elif file.id not in excluded:
            text_cunks, embedding_data = await embedder.text_to_embeddings(file.content)
            await documents_manager.recreate_documents(file.id, text_cunks, embedding_data)
