# Include the Dropbox SDK
import dropbox
import time
import datetime
import urllib
import os
import ConfigParser
import os.path
import shutil

# Get your app key and secret from the Dropbox developer website

class Otto:
	APP_KEY = ''
	APP_SECRET = '' 
	ACCESS_TOKEN = ''
	CHECK_DELAY = 60 #number of seconds before checking dropbox for updates
	CUR_REV = 0
	TORRENT_DIR = ''


	def getFile(self):
		"""
		Pull file from dropbox and assess if needs to be processed
		"""
		client = dropbox.client.DropboxClient(self.ACCESS_TOKEN)
		folder_metadata = client.metadata('/')
		if False:
			print "File Listings:"
			for item in folder_metadata['contents']:
				if not item['is_dir']:
					print item['path']

		f, metadata = client.get_file_and_metadata('/commands.conf')
		read_rev = metadata['revision']
		
		if read_rev > self.CUR_REV:
			print "[Processing rev "+str(read_rev)+"]"
			self.CUR_REV = read_rev
			self.processConf(f.read())
		else:
			print "... nothing to do"


	def authorise(self):
		"""
		Authorise against dropbox and return access token
		"""
		flow = dropbox.client.DropboxOAuth2FlowNoRedirect(self.APP_KEY, self.APP_SECRET)

		# Have the user sign in and authorize this token
		authorize_url = flow.start()
		print '1. Go to: ' + authorize_url
		print '2. Click "Allow" (you might have to log in first)'
		print '3. Copy the authorization code.'
		code = raw_input("Enter the authorization code here: ").strip()
		# This will fail if the user enters an invalid authorization code
		access_token, user_id = flow.finish(code)
		return access_token

	def processConf(self,content):
		"""
		Iterate through the pulled down config file
		"""
		lines = content.split('\n')
		for line in lines:
			print "[Processing] " + str(line)
			command,arg = line.split(' ')
			print "[Command] "+command
			print "[Arg] "+arg
			command = command.lower()
			if command == 'tor': 
				self.processTorrent(arg)
			elif command == 'com':
				processCom(arg)

	def processTorrent(self,torrent_url):
		"""
		Downloads torrent to the specified directory
		"""
		print "[Downloading torrent... "+str(torrent_url) + "]"
		testfile = urllib.URLopener()
		fh, headers = testfile.retrieve(torrent_url)
		filename = os.path.split(fh)[1]
		dest = os.path.join(self.TORRENT_DIR,filename)
		shutil.move(fh, dest)
		# print str(fh)
		print "[Complete] Torrent download Completed to "+str(dest)


	def execute(self):
		while True:
			st = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
			print str(st) + " checking dropbox..."
			otto.getFile()
			time.sleep(self.CHECK_DELAY)

	def firstTimeWizard(self,configfile):
		"""
		This gets directory info from user and also 
		guides user through authorising dropbox access
		"""
		
		if os.path.exists(configfile):
			print 'Using config file '+str(configfile)
			return True
		print "script dir = "+str(scriptdir)

		config = ConfigParser.RawConfigParser()
		config.add_section('dirs')
		config.add_section('dropbox')
		config.add_section('misc')

		config.set('misc', 'checkfrequency', 60)

		while self.APP_KEY == '':
			self.APP_KEY = raw_input("Enter Dropbox App Key: ").strip()
		config.set('dropbox', 'appkey', self.APP_KEY)

		while self.APP_SECRET == '':
			self.APP_SECRET = raw_input("Enter Dropbox App Secret: ").strip()
		config.set('dropbox', 'appsecret', self.APP_SECRET)

		self.ACCESS_TOKEN = self.authorise()
		if not self.ACCESS_TOKEN:
			print "Access token not received, exiting..."
			return False

		config.set('dropbox', 'accesstoken', self.ACCESS_TOKEN)
		print 'Access Token: '+str(self.ACCESS_TOKEN) + ' saved to config'

		torrentdir = raw_input("Enter torrent download dir:["+str(scriptdir)+"] ").strip()
		if not os.path.isdir(torrentdir):
			torrentdir = os.path.join(scriptdir,'torrents')
		config.set('dirs', 'torrentdir', torrentdir)

		# Writing our configuration file to 'example.cfg'
		with open(configfile, 'wb') as theconfigfile:
			config.write(theconfigfile)
		return True


	def readConfig(self,configfile):
		config = ConfigParser.RawConfigParser()
		config.read(configfile)
		self.ACCESS_TOKEN = config.get('dropbox','accesstoken')
		self.TORRENT_DIR = config.get('dirs','torrentdir')
		self.CHECK_DELAY = config.getint('misc','checkfrequency')
			

scriptdir = os.path.dirname(os.path.realpath(__file__))
configfile = os.path.join(scriptdir,'otto.conf')
otto = Otto()
if otto.firstTimeWizard(configfile):
	otto.readConfig(configfile)
	otto.execute()


