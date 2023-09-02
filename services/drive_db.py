from fastapi import Request
from typing import Sequence
import asyncio

from .drive import GDriveEventsManager, GDrive
from .db import DBDriveFiles, DBDocuments
from .llm.preprocessing import Embedder
import db.interfaces as I


async def db_drive_synchronization(event: Request):

    manager = GDriveEventsManager()
    files_mapping = await manager.HANDLER.handle_event(headers=event.headers)

    if not files_mapping:
        return

    drive_files_manager = DBDriveFiles()
    existing_files = await drive_files_manager.list_files(tuple(files_mapping.keys()))

    excluded = []  # File ids to exclude from re-embedding

    files_to_create = []
    files_to_update_from = []
    existing_files_for_update = []
    files_to_delete = []

    for existing_file in existing_files:

        file = files_mapping.pop(existing_file.file_id)

        if file.trashed:
            files_to_delete.append(file)
        else:
            files_to_update_from.append(file)
            existing_files_for_update.append(existing_file)
            if file.content == existing_file.content:
                excluded.append(file.id)

    files_to_create = list(files_mapping.values())

    await asyncio.gather(

        asyncio.create_task(drive_files_manager.create_files(
            files_to_create
        )),

        asyncio.create_task(drive_files_manager.update_files(
            zip(files_to_update_from, existing_files_for_update)
        )),

        asyncio.create_task(drive_files_manager.delete_files(
            files_to_delete
        )),
    )

    await embed_into_chunked_documents((*files_to_create, *files_to_update_from), files_to_delete, excluded)


async def embed_into_chunked_documents(files_to_embed: Sequence[I.File], files_to_delete: Sequence[I.File], excluded: Sequence[str]):

    embedder = Embedder(512, 32, 'OverlapOptimizer')
    documents_manager = DBDocuments()

    await documents_manager.delete_documents(files_to_delete)

    for file in files_to_embed:

        if file.id not in excluded:

            text_cunks, embedding_data = await embedder.text_to_embeddings(file.content)
            await documents_manager.create_documents(file.id, text_cunks, embedding_data)
