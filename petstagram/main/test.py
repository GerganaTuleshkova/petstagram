import re

text = "Random text Hello from shubhamg199630@gmail.com to priya@yahoo.com about the meeting @2PM, rghiuwfej " \
       "gigigig@dell.com next email with sample@dell.com"

emails_list = re.findall('\S+@\S+', text)
#emails_list = re.findall('\S+@dell\S+', text)
print(emails_list)