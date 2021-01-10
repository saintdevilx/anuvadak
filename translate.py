import argparse,sys, os
import json
import logging
import boto3
from botocore.exceptions import ClientError
from botocore.compat import six
from googletrans import Translator


class UploadToS3:
	def upload_file(self, file_name, bucket, object_name=None):
		"""Upload a file to an S3 bucket

		:param file_name: File to upload   - full path or relative path
		:param bucket: Bucket to upload to bucket name
		:param object_name: S3 object name. If not specified then file_name is used
		:return: True if file was uploaded, else False

		*** Configuration ***

		Before you can begin using Boto3, you should set up authentication credentials. Credentials for your AWS account can be found in the IAM Console. You can create or use an existing user. Go to manage access keys and generate a new set of keys.

		If you have the AWS CLI installed, then you can use it to configure your credentials file:

		aws configure
		Alternatively, you can create the credential file yourself. By default, its location is at ~/.aws/credentials:

		[default]
		aws_access_key_id = YOUR_ACCESS_KEY
		aws_secret_access_key = YOUR_SECRET_KEY
		You may also want to set a default region. This can be done in the configuration file. By default, its location is at ~/.aws/config:

		[default]
		region=us-east-1
		Alternatively, you can pass a region_name when creating clients and resources.

		This sets up credentials for the default profile as well as a default region to use when creating connections. See Configuration for in-depth configuration sources and options.		

		
		for more details go through this link : https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html

		"""

		# If S3 object_name was not specified, use file_name
		if object_name is None:
			object_name = file_name.split('/')[-1]

		# Upload the file
		s3_client = boto3.client('s3')
		try:
			response = s3_client.upload_file(str(file_name), bucket, object_name,
				ExtraArgs={'ACL': 'public-read'})
		except ClientError as e:
			logging.error(e)
			return False
		print(F'{object_name} uploaded successfully')
		return True	

	def upload_all_file(self):
		files_list = os.listdir('out/')
		for _file in files_list:
			name, ext = _file.split('.')
			if name in TranslateJSON.lang:
				self.upload_file(F"out/{_file}")


class TranslateJSON:
	EN = 'en'

	# indian languages 
	# can be configured to use any google translate langauge shortcode
	# currently using only indian language
	lang = ['pa', 'gu', 'mr','ta','ka','ml','be','te']

	# default input file 
	in_file = 'en_IN.json'

	# output directory 
	out_file = 'out/'
	google_translator = None


	def translate(self, langs, load_dump=False):
		trans_text = ""
		with open(self.in_file) as fp:
			res = json.load(fp)
			keys = res.keys()

			for l in langs:
				values = list(res.values())
				print(F'translating ... to {l} ')
				translated = self.google_trans(values, dest=l)
				data = dict(zip(keys, translated))
				with open(F"out/{l}.json",  'w+') as fp:
					json.dump(data, fp, ensure_ascii=False)


	def main(self):
		parser = argparse.ArgumentParser()
		parser.add_argument('--lang', help=F"translate into language type {self.lang}")
		parser.add_argument('--infile', help=F"file that will be used to translate")
		parser.add_argument('--upload', help='upload file to s3 directly , `all` will auto upload all the files exists in `out` directory ')
		args = parser.parse_args()	

		if args.infile:
			self.in_file = args.infile	 

		if args.lang:
			lang_args = args.lang.split(',')
			if lang_args[0] == 'all':
				self.translate(self.lang, load_dump=load_dump)		
			elif len(set(self.lang) - set(args.lang)) < len(self.lang):
				print("--lang not supported")
				sys.exit(0)
			else:
				self.translate(lang_args)

		if args.upload:
			if args.upload =='all':
				UploadToS3().upload_all_file()
			else:	
				UploadToS3().upload_file(str(args.upload))				

	def google_trans(self, values, dest='en'):
		char_count = 0
		res = []
		i=0
		start = 0
		print(F'translating to `{dest}`')

		if not self.google_translator:
			self.google_translator = Translator()		

		while i< len(values):
			start = i
			while i< len(values) and char_count <= 2000:
				char_count += len(values[i])
				if char_count<2000:
					i+=1
			text = "\n".join(values[start:i])
			char_count = 0
			translated =  self.google_translator.translate(text, src='en', dest=dest)
			res += translated.text.split('\n')
		return res



if __name__=="__main__":
	translate = TranslateJSON()
	translate.main()