# -*- coding: utf-8 -*-

# import modules
import os
import sys
import argparse
import time
from utils import (
	log_management
)
if os.name == 'nt':
	copy = 'copy'
else:
	copy = 'cp'
#defino argumentos de script
'''
Arguments

'''

parser = argparse.ArgumentParser(description='Arguments.')

'''
Output
'''
parser.add_argument(
	'--output',
	'-o',
	type=str,
	required = False,
	default = './data',
	help='Folder to save collected data. Default: `./data`'
)
'''
max-msgs
'''
parser.add_argument(
	'--max-msgs',
	type=int,
	required=False,
	help='Maximum number of messages to download. Default: all messages'
)
# parse arguments
args = vars(parser.parse_args())
data_path = args['output']
exit = 'n'
if args['max_msgs']:
	max_msgs = args['max_msgs']
	limit = f'--max-msgs {max_msgs}'
	
try:
	while exit != 'y':
		print ('--------------------------------')
		print ('What function do you want to run?')
		print ('--------------------------------')
		print ('1. Get a channel')
		print ('2. Get a snowball from a user')
		print ('3. Get a channel group')
		print ('4. Exit')
		print (' ')
		while True:
			try:
				option = int(input('--> Enter option: '))
				if option in range (1,5):
					break
				else:
					print('type a number from 1 to 4')
			except:
				print('type a number from 1 to 4')
			'''
			Get a channel
			'''
		if option == 1:
			channel = input ('Enter channel name: ')
			path_channel = f'{data_path}/{channel}'
			print(f'Output on {path_channel}')
			print(f'Download channel {channel}')
			os.system(f'python main.py --telegram-channel {channel} {limit} --output {path_channel}')
			# Convertir json en csv y excel y ordenar de mensaje más reciente a más antiguo
			print(f'Building the {channel} message csv')
			os.system(f'python build-dataset.py --telegram-channel {channel}  --data-path  {path_channel}')
		'''
		Get a snowball from a user
		'''
		if option == 2:
			root_channel = input ('root channel (must have been downloaded before): ')
			path_channel = f'{data_path}/{root_channel}'
			path_channel_nor = os.path.normpath(path_channel)
			path_channel_n2 = f'{data_path}/{root_channel}_n2'
			path_channel_n2_nor = os.path.normpath(path_channel_n2)
			related_channels_nor = os.path.normpath(f'{path_channel}/related_channels.csv')
			if not os.path.exists(related_channels_nor):
				print(f'{root_channel} must have been downloaded before')
			else:
				os.makedirs(path_channel_n2_nor, exist_ok=True)
				(f_log, list_downloaded, list_json_csv) = log_management(f'{path_channel_n2}/{root_channel}_n2_log.csv')
				with open(related_channels_nor, 'r') as inputfile:
					channels = inputfile.readlines()
					num_channels = len (channels)
					i = 0
					for channel in channels:
						i = i + 1
						channel = channel.strip('\n') # quitar salto de línea
						if not channel in list_downloaded.values:
							print(f'--------> downloading {channel} ({i} of {num_channels})')
							os.system(f'python main.py --telegram-channel {channel} {limit} --output {path_channel_n2}')
							f_log.write(f'{channel},downloaded,{time.ctime()}\n')
							f_log.flush()
						else:
							print(f'--------> already downloaded {channel} ({i} of {num_channels})')
						if not channel in list_json_csv.values:
					# convertir json en csv y excel
							print(f'Building the {channel} message csv')
							os.system(f'python build-dataset.py --telegram-channel {channel} --data-path  {path_channel}_n2')
							f_log.write(f'{channel},json_csv,{time.ctime()}\n')
							f_log.flush()
						else:
							print(f'--------> already flattened {channel} ({i} of {num_channels})')
					f_log.close()
			'''
			Get a channel group
			'''
		if option == 3:
			group = input ('Enter group name: ')
			path_group = f'{data_path}/{group}'
			path_group_nor = os.path.normpath(path_group)
			file_list_channels_nor = os.path.normpath(f'{path_group}/list_channels.csv')
			if not os.path.exists(file_list_channels_nor):
				os.makedirs(path_group_nor, exist_ok=True)
				group_file = input ('Enter channel group file name (one channel per line): ')
				group_file_nor = os.path.normpath(group_file)
				print (f' {copy} {group_file_nor} {file_list_channels_nor}')
				os.system (f' {copy} {group_file_nor} {file_list_channels_nor}')
			(f_log, list_downloaded, list_json_csv) = log_management(f'{path_group}/{group}_log.csv')
			with open(file_list_channels_nor, 'r') as inputfile:
				channels = inputfile.readlines()
			num_channels = len (channels)
			i = 0
			for channel in channels:
				i = i + 1
				channel = channel.strip('\n') # quitar salto de línea
				if not channel in list_downloaded.values:
					print(f'--------> downloading {channel} ({i} of {num_channels})')
					os.system (f'python main.py --telegram-channel {channel} {limit} --output {path_group}')
					f_log.write(f'{channel},downloaded,{time.ctime()}\n')
					f_log.flush()
				else:
					print(f'--------> already downloaded {channel} ({i} of {num_channels})')
				# convertir json en csv y excel
				if not channel in list_json_csv.values:
					print(f'Building the {channel} message csv')
					os.system (f'python build-dataset.py --telegram-channel {channel} --data-path  {path_group}')
					f_log.write(f'{channel},json_csv,{time.ctime()}\n')
					f_log.flush()
				else:
					print(f'--------> already flattened {channel} ({i} of {num_channels})')
			f_log.close()
			'''
			Exit
			'''
		elif option == 4:
			exit = 'y'
			break
except KeyboardInterrupt:
	print ('\nGoodbye!')
	sys.exit(0)



