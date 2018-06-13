import argparse
import requests
import base64
import json
import sys
import csv
import pip
import os

# [START install_routine]
def install(package):
    pip.main(['install', package])

    print('just installed %s, please rerun this script at your convenience' % package)
    sys.exit(1)
# [END install_routine]

try:
    from progress.bar import Bar
    from progress.spinner import Spinner
except ImportError:
    print('progress is not installed, installing it now!')
    install('progress')


# [START config]
API_KEY = ""
MAX_RESULTS = 10

API_URI= 'https://vision.googleapis.com/v1/images:annotate?key='
# [END config]

IMG_EXTENSIONS = ['.jpg', '.jpeg', '.bmp', '.png']
CONTENT_TYPE = 'application/json'
DETECTION_TYPES = [
    'TYPE_UNSPECIFIED',
    'FACE_DETECTION',
    'LANDMARK_DETECTION',
    'LOGO_DETECTION',
    'LABEL_DETECTION',
    'TEXT_DETECTION',
    'SAFE_SEARCH_DETECTION',
    'IMAGE_PROPERTIES'
]

# [START main]
def main(input_path, output_filename):
  """
    Google Vison API to CSV
  """

  # collect images from path
  images = []
  spinner = Spinner(('collect images from %s  ' % input_path))
  for current_file in os.listdir(input_path):
    if current_file.endswith('.jpg'):
      images.append(current_file)
    spinner.next()
  spinner.finish()

  # analyze images with Google Vision API
  responses = []
  bar = Bar('analyze images', max=len(images))
  for current_img in images:
    request = generate_request(input_path + '/' + current_img)
    response = call_api(request)
    responses.append({
      'file': current_img,
      'response': response
    })
    bar.next()
  bar.finish()
  #print(json.dumps(responses, indent=4))

  create_csv(responses, output_filename)
  
# [END main]

# [START generate_csv]
def create_csv(result, csv_filename):
  spinner = Spinner(('create CSV file to %s  ' % csv_filename))
  with open(csv_filename, 'w') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerow(['FILE', 'LABEL_1', 'LABEL_2', 'DOMINANT_COLOR_RGB'])
    for response in result:
        #print(response)
        row = [
          response['file'],
          response['response']['responses'][0]['labelAnnotations'][0]['description'],
          response['response']['responses'][0]['labelAnnotations'][1]['description'],
          "(%s, %s, %s)" % (
            response['response']['responses'][0]['imagePropertiesAnnotation']['dominantColors']['colors'][1]['color']['red'],
            response['response']['responses'][0]['imagePropertiesAnnotation']['dominantColors']['colors'][1]['color']['green'],
            response['response']['responses'][0]['imagePropertiesAnnotation']['dominantColors']['colors'][1]['color']['blue'],
          )
        ]
        #print(row)

        writer.writerow(row)
        spinner.next()
    spinner.finish()
# [END generate_csv]

# [START generate_request]
def generate_request(img):
  # init new request list
  request_list = []

  with open(img, 'rb') as image_file:
    content_json_obj = {
        'content': base64.b64encode(image_file.read()).decode('UTF-8')
    }

  feature_json_obj = []
  feature_json_obj.append({
    'type': DETECTION_TYPES[4],
    'maxResults': MAX_RESULTS,
  })
  feature_json_obj.append({
    'type': DETECTION_TYPES[7],
  })

  request_list.append({
      'features': feature_json_obj,
      'image': content_json_obj,
  })

  #print(json.dumps({'requests': request_list}, indent=4))
  return json.dumps({'requests': request_list})
# [END generate_request]

# [START api_request]
def call_api(request_data):
  response = requests.post(
    url     = API_URI + API_KEY,
    data    = request_data,
    headers = {
      'Content-Type': CONTENT_TYPE
    })

  if response.status_code == 200:
    return json.loads(response.text)
  else:
    sys.exit('Error during request.\nStatus Code: %s\nResponse: %s' % (response.status_code, response.text))
# [END api_request]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '-i', dest='input_file', required=True,
        help='The input folder with all images to convert to json.')
    parser.add_argument(
        '-o', dest='output_file', required=True,
        help='The name of the json file to output to.')
    args = parser.parse_args()

    main(args.input_file, args.output_file)