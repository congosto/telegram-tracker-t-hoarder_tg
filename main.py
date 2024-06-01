# -*- coding: utf-8 -*-

# import modules
import pandas as pd
import argparse
import asyncio
import nest_asyncio # change by congosto
import json
import time
import sys
import os
# import submodules
from tqdm import tqdm
# import submodules
# import Telegram API submodules
from api import *
from utils import (
	get_config_attrs, JSONEncoder, create_dirs, 
	write_collected_chats,get_last_download_context,
	put_last_download_context,store_channels_download,store_channels_related
)



'''

Arguments

'''

parser = argparse.ArgumentParser(description='Arguments.')
parser.add_argument(
	'--telegram-channel',
	type=str,
	required=True,
	help='Specifies a Telegram Channel.'
)

parser.add_argument(
	'--limit-download-to-channel-metadata',
	action='store_true',
	help='Will collect channels metadata only, not posts data.'
)

# chaged by congosto
'''

max-msgs
'''
parser.add_argument(
	'--max-msgs',
	type=int,
	required=False,
	help='Maximum number of messages to download. Default: all messages'
)

'''

Output
'''
parser.add_argument(
	'--output',
	'-o',
	type=str,
	required=False,
	help='Folder to save collected data. Default: `./output/data`'
)


# parse arguments
args = vars(parser.parse_args())
config_attrs = get_config_attrs()

args = {**args, **config_attrs}

# log results
text = f'''
Init program at {time.ctime()}

'''
print (text)


'''

Variables

'''

# Telegram API credentials

'''

FILL API KEYS
'''
sfile = 'session_file'
api_id = args['api_id']
api_hash = args['api_hash']
phone = args['phone']

# event loop
# Change by congosto
nest_asyncio.apply()
loop = asyncio.get_event_loop()

# data collection
counter = {}

'''

> Get Client <API connection>

'''

# get `client` connection
client = loop.run_until_complete(
	get_connection(sfile, api_id, api_hash, phone)
)

# request type
channel = args['telegram_channel']

# chaged by congosto
# reading | max-msgs
if args['max_msgs']:
	max_msgs = args['max_msgs']
	limited_msgs = True
else:
	limited_msgs = False
	max_msgs = 0  # not limitedf

# reading | Creating an output folder
if args['output']:
	output_folder = args['output']
	if output_folder.endswith('/'):
		output_folder = output_folder[:-1]
	else:
		pass
else:
	output_folder = './output/data'

# create dirs
create_dirs(output_folder)


'''

Methods

- GetHistoryRequest
- SearchGlobalRequest

'''

#change by congosto
'''
Channels are downloaded one by one
'''
	
# add by congosto
'''
get context download
'''
(start_msg,num_msgs_downloaded) = get_last_download_context(f'{output_folder}/{channel}/log_downloads.csv')

'''

Process arguments
-> channels' data

-> Get Entity <Channel's attrs>
-> Get Full Channel request.
-> Get Posts <Request channels' posts>

'''

# new line
print ('')
print (f'> Collecting data from Telegram Channel -> {channel}')
print ('> ...')
print ('')

# Channel's attributes
entity_attrs = loop.run_until_complete(
	get_entity_attrs(client, channel)
)



if entity_attrs:

	# Get Channel ID | convert output to dict
	channel_id = entity_attrs.id
	entity_attrs_dict = entity_attrs.to_dict()

	# Collect Source -> GetFullChannelRequest
	channel_request = loop.run_until_complete(
		full_channel_req(client, channel_id)
	)

	# save full channel request
	full_channel_data = channel_request.to_dict()

	# JsonEncoder
	full_channel_data = JSONEncoder().encode(full_channel_data)
	full_channel_data = json.loads(full_channel_data)

	# save data
	print ('> Writing channel data...')
	create_dirs(output_folder, subfolders=channel)
	file_path = f'{output_folder}/{channel}/{channel}.json'
	channel_obj = json.dumps(
		full_channel_data,
		ensure_ascii=False,
		separators=(',',':')
	)
	writer = open(file_path, mode='w', encoding='utf-8')
	writer.write(channel_obj)
	writer.close()
	print ('> done.')
	print ('')

	# collect chats
	chats_path = f'{output_folder}/chats.txt'
	chats_file = open(chats_path, mode='a', encoding='utf-8')

	# channel chats
	counter = write_collected_chats(
	full_channel_data['chats'],
		chats_file,
		channel,
		counter,
		'channel_request',
		client,
		output_folder
	)
	last_msg = start_msg
	num_msgs = 0
	min_id = start_msg
	if not args['limit_download_to_channel_metadata']:
		# Collect posts
		if start_msg == 0: # changed by congosto
			print('Downloading all messages')
			posts = loop.run_until_complete(
				get_posts(client, channel_id)
			)

		else:
			print(f'Downloading from msg {start_msg}')
			posts = loop.run_until_complete(
				get_posts(client, channel_id, min_id=min_id)
			)

		data = posts.to_dict()
		# Change by Congosto
		'''
		get most recent msg 
		'''
		pbar_flag = False
		if len(posts.messages) > 0:
			offset_id = min([i['id'] for i in data['messages']])
			last_msg = data['messages'][0]['id']
			num_msgs = len(posts.messages)
			pbar = tqdm(total=last_msg - start_msg)
			pbar.set_description(f'Downloading posts')
			pbar_flag = True
		# Get offset ID | Get messages
		while len(posts.messages) > 0:

			if start_msg > 0: # changed by congosto
				posts = loop.run_until_complete(
					get_posts(
						client,
						channel_id,
						min_id=min_id,
						offset_id=offset_id
					)
				)	
			else:
				posts = loop.run_until_complete(
					get_posts(
						client,
						channel_id,
						offset_id=offset_id
					)
				)
			# Update data dict
			if posts.messages:
				tmp = posts.to_dict()
				data['messages'].extend(tmp['messages'])

				# Adding unique chats objects
				all_chats = [i['id'] for i in data['chats']]
				chats = [
					i for i in tmp['chats']
					if i['id'] not in all_chats
				]
				# channel chats in posts
				counter = write_collected_chats(
					tmp['chats'],
					chats_file,
					channel,
					counter,
					'from_messages',
					client,
					output_folder
				)
				# Adding unique users objects
				all_users = [i['id'] for i in data['users']]
				users = [
					i for i in tmp['users']
					if i['id'] not in all_users
				]
				# extend UNIQUE chats & users
				data['chats'].extend(chats)
				data['users'].extend(users)
				# Get offset ID
				offset_id = min([i['id'] for i in tmp['messages']])
				# Change by Congosto
				'''
				get most recent msg and show post downloaded
				'''
				num_msgs = num_msgs + len(posts.messages)
				#if os.name == 'nt':
				#	print(f'\x1b[2K{num_msgs} downloaded', end='\r')
				#	#print(f'\x1b{num_msgs} downloaded', end='\r')
				#else:
				#	if num_msgs % 5000 == 0:
				#		print(f'{num_msgs} downloaded\r')
				pbar.update(len(posts.messages))
				if limited_msgs & (num_msgs >= max_msgs):
					break
		# JsonEncoder
		# Close pbar connection
		if pbar_flag:
			pbar.close()
		data = JSONEncoder().encode(data)
		data = json.loads(data)

		# save data
		print ('> Writing posts data...')
		file_path = f'{output_folder}/{channel}/{channel}_messages.json'
		obj = json.dumps(
			data,
			ensure_ascii=False,
			separators=(',',':')
		)
			
		# writer
		writer = open(file_path, mode='w', encoding='utf-8')
		writer.write(obj)
		writer.close()

	'''

	Channels not found
	'''
	exceptions_path = f'{output_folder}/_exceptions-channels-not-found.txt'
	w = open(exceptions_path, encoding='utf-8', mode='a')
	w.write(f'{channel}\n')
	w.close()

'''

Clean generated chats text file

'''

# close chat file
chats_file.close()

# get collected chats
collected_chats = list(set([
	i.rstrip() for i in open(chats_path, mode='r', encoding='utf-8')
]))

# re write collected chats
chats_file = open(chats_path, mode='w', encoding='utf-8')
for c in collected_chats:
	chats_file.write(f'{c}\n')

# close file
chats_file.close()


# Process counter
counter_df = pd.DataFrame.from_dict(
	counter,
	orient='index'
).reset_index().rename(
	columns={
		'index': 'id'
	}
)

# save counter
counter_df.to_csv(
	f'{output_folder}/counter.csv',
	encoding='utf-8',
	index=False
)

# merge dataframe
df = pd.read_csv(
f'{output_folder}/collected_chats.csv',
encoding='utf-8'
)

#del counter_df['username'] # Change by Congosto
#remove possible duplicates
df.drop_duplicates(subset=['id'], keep='first', inplace=True) # Change by Congosto
df.to_csv(
	f'{output_folder}/collected_chats.csv',
	mode='w', # Change by Congosto  avoid duplicates
	index=False,
	encoding='utf-8'
)

# Change by Congosto
'''
Save names of related channels
'''
users_names = df["username"]
users_names.to_csv(
	f'{output_folder}/related_channels.csv',
	mode='w', 
	header=False,
	index=False,
	encoding='utf-8'
)
df = df.merge(counter_df, how='left', on='id')
'''
The metadata and counters are saved in collected_chats_full.csv,
to avoid problems when making 
 successive merges when extracting the channel data again
'''
df.to_csv(
	f'{output_folder}/collected_chats_full.csv',
	mode='w', # Change by Congosto para que no duplique entradas
	index=False,
	encoding='utf-8'
)
'''
The metadata and counters are saved in collected_chats_full.csv,
to avoid problems when making 
 successive merges when extracting the channel data again
'''
df.to_csv(
	f'{output_folder}/collected_chats_full.csv',
	mode='w', 
	index=False,
	encoding='utf-8'
)
# changed by congosto
'''
Save downloaded context
'''
put_last_download_context(f'{output_folder}/{channel}/log_downloads.csv',time.ctime(),last_msg,num_msgs)


# changed by congosto
'''
Save collected_channel
'''

store_channels_download(f'./{output_folder}/collected_channel_all.csv',channel,output_folder)
# log results
# changed by congosto
'''
Save related_channel
'''
store_channels_related(f'./{output_folder}/related_channel_all.csv',users_names,output_folder)

# log results
text = f'End program at {time.ctime()}'

print (text)
