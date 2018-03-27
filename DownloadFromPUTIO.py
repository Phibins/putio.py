import putiopy
import os

KB = 1024
MB = 1024 * KB

OAUTH_TOKEN = 'xxx'
CLIENT_SECRET = 'xxx'
CLIENT_ID = 1
# Read and write operations are limited to this chunk size.
# This can make a big difference when dealing with large files.
CHUNK_SIZE = 256 * KB * 10
#destination folder on NAS
dest='/volume1/homes/Phillip/Media/Unsorted'


# this will open a browser to authetication url
# after authenticating you will find the oauth_token in the address bar
helper = putiopy.AuthHelper(CLIENT_ID,CLIENT_SECRET,'', type='token')
helper.open_authentication_url()
client = putiopy.Client(OAUTH_TOKEN)

# list all files on put.io
files = client.File.list()
for n in files: 
	if n.name == 'Plex':
		#Get Plex File and its size
		Plex_File = n

#If the plex folder contains data, download it and run filebot
if Plex_File.size>0:
	# Delete the files on put.io when download completes? (does not delete directories)
	delete_after_download=False
	# Download command
	download = Plex_File.download(dest,delete_after_download,CHUNK_SIZE)

	FILEBOTSCRIPT="filebot -script fn:amc --log INFO --output \"/volume1/Media\" --action move --conflict auto -non-strict \"/volume1/homes/Phillip/Media/Unsorted\" --filter \"(n != \'American Dad!\' || s == 15)\" --log-file amc.log --def clean=y music=y subtitles=en musicFormat=\"{plex}\" movieFormat=\"{plex}\" seriesFormat=\"{plex}\" minFileSize=4"
	os.system(FILEBOTSCRIPT)

	
	
	
## Test filebot command
#echo $'filebot -script fn:amc --log INFO --output \"/volume1/Media\" --action move --conflict auto -non-strict \"/volume1/homes/Phillip/Media/Unsorted\" --filter \"(n != \'American Dad!\' || s == 15)\" --log-file amc.log --def clean=y music=y subtitles=en musicFormat=\"{plex}\" movieFormat=\"{plex}\" seriesFormat=\"{plex}\" minFileSize=4'