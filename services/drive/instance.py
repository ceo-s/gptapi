# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive, GoogleDriveFile, GoogleDriveFileList
# from pprint import pp

# gauth = GoogleAuth()
# gauth.LocalWebserverAuth(port_numbers=[8000])

# drive = GoogleDrive(gauth)
# files_list: GoogleDriveFileList = drive.ListFile().GetList()

# # file: GoogleDriveFile = files_list[2]
# BASEDIR_ID = "1f7o4aD60tka0ehhv4WuSaeQ-2Uy-mAN0"
# BASEDIR = drive.CreateFile({"id": BASEDIR_ID})
# BASEDIR.FetchMetadata()

# # pp(BASEDIR.metadata)

# file_list = drive.ListFile(
#     {'q': f"'{BASEDIR_ID}' in parents and trashed=false"}).GetList()

# for folder in file_list:
#     ...

# pp(drive.dirty)
