# -*- coding: utf-8 -*-
from __future__ import print_function
import examples.config as cf
import telebot
import time


import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None




def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(cf.CLIENT_SECRET_FILE, cf.SCOPES)
        flow.user_agent = cf.APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def read_cell_spreadsheet(rangeName):
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())

	service = discovery.build('sheets', 'v4', http=http,
							  discoveryServiceUrl=cf.discoveryUrl)

	result = service.spreadsheets().values().get(
		spreadsheetId=cf.spreadsheetId, range=rangeName).execute()
	values = result.get('values', [])


	if not values:
		print('No data found.')
	else:
		print('Name, Major:')
		for row in values:
			# Print columns A and E, which correspond to indices 0 and 4.
			print('%s' % (row[0]))
			return row[0]

def read_rows_spreadsheet(rangeName):
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())

	service = discovery.build('sheets', 'v4', http=http,
							  discoveryServiceUrl=cf.discoveryUrl)

	result = service.spreadsheets().values().get(
		spreadsheetId = cf.spreadsheetId, range=rangeName).execute()
	values = result.get('values', [])

	if not values:
		print('No data found.')
	else:
		return values

def write_spreadsheet(message):

	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	message_fields = convert_msg_to_sheet(message)
	service = discovery.build('sheets', 'v4', http=http,
							  discoveryServiceUrl=cf.discoveryUrl)

	rangeName = 'A1:F1'

	values = [
		message_fields  # cell vales
		# Additional rows ...

	]

	value_range_body = {
		# TODO: Add desired entries to the request body.
		'values':values
	}

	request = service.spreadsheets().values().append(spreadsheetId=cf.spreadsheetId, range=rangeName,
													 valueInputOption=cf.value_input_option,
													 insertDataOption=cf.insert_data_option, body=value_range_body)
	response = request.execute()
	print(response)

def convert_msg_to_sheet(message):
	sheet_row = []
	sheet_row.append(time.strftime('%x %X')) # set datetime
	sheet_row.append(message.from_user.first_name) #user name

	body = message.text.split(' ')

	sheet_row.append(body[0]) #placeholder for command
	sheet_row.append(body[1]) #placeholder for product name
	sheet_row.append(float(body[2])) #placeholder for cost
	sheet_row.append(' '.join(body[3:])) #placeholder for comment

	return sheet_row

def errhandler (message):
	bot.send_message(message.chat.id, cf.UNKNOWN_COMMAND)

def run_bot_command(message):
	body = message.text.split(' ')
	command = body[0] #"/expences"
	takeaction[command](message)

def save_input_to_sheet(message):
	write_spreadsheet(message)
	bot.send_message(message.chat.id, message.text + ' confirmed')

def get_help(message):
	msg = 'list of command: \n'+' \n'.join(takeaction.keys()) +'\n ' +cf.HELP_MSG
	bot.send_message(message.chat.id, msg)

def get_sheet_link(message):
	bot.send_message(message.chat.id, 'sheet link: '+cf.LINK_SHEET_BASE+cf.spreadsheetId)

def get_current_week_report(message):
	bot.send_message(message.chat.id, cf.COMMAND_IN_DEV_MSG)

def get_last10_report(message):
	rows = read_rows_spreadsheet('A2:F')
	msg = ' list of last 10 inputs: \n'
	num = 10
	if len(rows)<10: num=len(rows)
	for cell in rows[:num]:
		msg = msg + ' '.join(cell) + '\n'
	bot.send_message(message.chat.id, msg)

def get_total(message):
	total = read_cell_spreadsheet('I1') # TODO remove hardcode #https://docs.google.com/spreadsheets/d/1-iKub0vWhJ4RTIyiKJ-F_J8FdEVFovilD258XJHURRw/edit#gid=0&range=H2
	bot.send_message(message.chat.id, ' your family total: ' +str(total))

bot = telebot.TeleBot(cf.token)
# TODO create configuration dialog

takeaction = {
    "/exp": save_input_to_sheet,
    "/help": get_help,
    "/sheet": get_sheet_link,
	"/week": get_current_week_report,
    "/last10": get_last10_report,
	"/total":get_total
}

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
	#print message.text
	try:
		run_bot_command(message)
	except Exception,e:
		bot.send_message(message.chat.id, cf.ERR_MSG)
		print('ERROR: '+str(e))


if __name__ == '__main__':
	bot.polling(none_stop=True)

