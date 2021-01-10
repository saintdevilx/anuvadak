# anuvadak(translator)

A very small utility to translate `json` file based localization dictionary to different languages using google translate.

A very useful tool if you are builing any localization based app which required to translated in many different languages, for example india has more than 10 official langauges. to build an app for diffrent language speaker this tool would be very useful.
all you just have to make sure to keep one language(recommended) to build an app instead of focusing on other different langauges.

to install dependency

`
pip install -r requirements.txt
`

to simply use this tool
e.g. to translate to `punjabi`
`python translate.py --lang pa`

also have an option to directly upload to AWS S3 in case you are hosting your json file on S3.
e.g. to upload `pa.json ` to directly upload to S3

`python translate.py --upload out/pa.json`

in order to use AWS S3 upload you need to configure your credentials
you can create the credential file yourself. By default, its location is at ~/.aws/credentials:

  `[default]`
  
  `aws_access_key_id = YOUR_ACCESS_KEY`
  
  `aws_secret_access_key = YOUR_SECRET_KEY`
  

You may also want to set a default region. This can be done in the configuration file. 
By default, its location is at ~/.aws/config:

`[default]`
`region=us-east-1`
