# from flask import Flask, request, render_template_string
# import os
# import werkzeug.utils
# import boto3
# import logging
# import requests

# # Setup
# UPLOAD_FOLDER = 'uploads'
# ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
# BUCKET_NAME = 'input-textract-jahnavi'  # Replace with your S3 bucket name

# # Ensure the upload folder exists
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # Initialize Flask app
# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # HTML template for the app
# HTML_TEMPLATE = """
# <!doctype html>
# <html lang="en">
# <head>
#   <meta charset="utf-8">
#   <meta name="viewport" content="width=device-width, initial-scale=1">
#   <title>File Processing with AWS Textract and Polly</title>
#   <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
#   <style>
#     body { background: linear-gradient(to right, #6a11cb 0%, #2575fc 100%); color: #fff; }
#     .container, .navbar { max-width: 1200px; margin: auto; }
#     .card { margin-top: 2rem; background-color: rgba(255, 255, 255, 0.9); }
#     .custom-file-label::after { content: "Browse"; }
#     .navbar .nav-link { color: #fff !important; }
#     section { padding: 2rem 0; }
#     .white { color: #000; background-color: rgba(255, 255, 255, 0.8); padding: 20px; border-radius: 8px; margin-bottom: 20px; }
#   </style>
# </head>
# <body>
#   <nav class="navbar navbar-expand-lg navbar-dark">
#     <a class="navbar-brand" href="#">AWS Services</a>
#     <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
#       <span class="navbar-toggler-icon"></span>
#     </button>
#     <div class="collapse navbar-collapse" id="navbarNav">
#       <ul class="navbar-nav">
#         <li class="nav-item">
#           <a class="nav-link" href="#textract">Textract</a>
#         </li>
#         <li class="nav-item">
#           <a class="nav-link" href="#polly">Polly</a>
#         </li>
#       </ul>
#     </div>
#   </nav>

#   <div class="container">
#     <section id="upload">
#       <div class="card">
#         <div class="card-body">
#           <h1 class="card-title mb-4">Upload a File</h1>
#           <form action="" method="post" enctype="multipart/form-data">
#             <div class="custom-file mb-4">
#               <input type="file" class="custom-file-input" name="file" id="file">
#               <label class="custom-file-label" for="file">Choose file</label>
#             </div>
#             <button type="submit" class="btn btn-dark btn-block">Upload</button>
#           </form>
#           {% if filename %}
#             <div class="alert alert-success" role="alert">
#               Successfully uploaded: {{ filename }}
#             </div>
#           {% elif filename == "" %}
#             <div class="alert alert-danger" role="alert">
#               File format not allowed.
#             </div>
#           {% endif %}
#         </div>
#       </div>
#     </section>

#     <section id="info" class="white">
#       <h2>How It Works</h2>
#       <p>Transform your documents into lifelike speech with just a few clicks. Our service seamlessly combines the power of AWS Textract and Polly to convert written text into spoken words, making content more accessible for everyone. Here's how you can turn your documents into audio:</p>
#       <ol>
#         <li><strong>Upload Your Document:</strong> Start by uploading the document you wish to convert. We support a variety of formats including PDF, JPEG, PNG, and more. Please note that the maximum file size allowed is 10MB.</li>
#         <li><strong>Text Extraction with AWS Textract:</strong> Upon upload, AWS Textract springs into action, meticulously extracting text from your document. It can accurately identify, read, and interpret text and data, even from forms and tables.</li>
#         <li><strong>Text to Speech Conversion with AWS Polly:</strong> The extracted text is then transformed into natural-sounding speech using AWS Polly. This service allows for a high degree of customization, offering dozens of voices across a range of languages.</li>
#         <li><strong>Access Your Audio:</strong> Once converted, the audio file is ready for you. You can download the file directly from our site, receive it as an email attachment, or access it through your user dashboard.</li>
#       </ol>
#     </section>

#     <section id="textract" class="white">
#       <h2>AWS Textract</h2>
#       <p>AWS Textract is a fully managed machine learning service that automatically extracts text, handwriting, and data from scanned documents. Going beyond simple OCR, Textract can identify, read, and interpret text and data, even from forms and tables, making it an essential tool for digital document processing.</p>
#     </section>

#     <section id="polly" class="white">
#       <h2>AWS Polly</h2>
#       <p>AWS Polly is a cloud service that turns text into lifelike speech, allowing you to create applications that can talk. Powered by advanced deep learning technologies, Polly offers dozens of lifelike voices across a broad range of languages, enabling the development of new categories of speech-enabled products.</p>
#     </section>
#   </div>

#   <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
#   <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
#   <script>
#     // Update the file label after file select
#     $('.custom-file-input').on('change',function(){
#       var fileName = $(this).val().split('\\').pop();
#       $(this).next('.custom-file-label').addClass("selected").html(fileName);
#     })
#   </script>
# </body>
# </html>
# """

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# def upload_to_s3(file_name, bucket, object_name=None):
#     if object_name is None:
#         object_name = file_name
#     s3_client = boto3.client('s3')
#     try:
#         response = s3_client.upload_file(file_name, bucket, object_name)
        
#     except boto3.exceptions.S3UploadFailedError as e:
#         logging.error(e)
#         return False
#     return True


# def get_api_gateway_invoke_url(api_name, stage_name):
#     # Correctly initialize the API Gateway client
#     client = boto3.client('apigateway', region_name='us-east-1')  
#     response = client.get_rest_apis(limit=1000)

#     # Loop through the API Gateway instances to find a match
#     for item in response['items']:
#         if item['name'] == api_name:
#             api_id = item['id']
#             # Dynamically get the region for the invoke URL
#             #region_name = client.meta.region_name
#             invoke_url = f'https://{api_id}.execute-api.{'us-east-1'}.amazonaws.com/{stage_name}'
#             return invoke_url

#     # Return None if no API Gateway matches the provided name
#     return None

# @app.route('/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         file = request.files.get('file')
#         if file and allowed_file(file.filename):
#             filename = werkzeug.utils.secure_filename(file.filename)
#             file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(file_path)

#             upload_successful = upload_to_s3(file_path, BUCKET_NAME, filename)
            
#             print(upload_successful)
#             api_gateway_url = get_api_gateway_invoke_url('JahnaviApiGateway', 'prod')  # Using your API name and stage

#             if api_gateway_url:
#                     data = {
#                     "input_bucket": BUCKET_NAME,
#                     "input_bucket_file": filename
#                     }
#                     response = requests.post(api_gateway_url + '/textract-polly', json=data)  # Append your resource path if needed
#                     message = f"Successfully uploaded: {filename}"
#             else:
#                     message = "Failed to upload to S3."
#             return render_template_string(HTML_TEMPLATE, filename=filename, message=message)
#         else:
#             return render_template_string(HTML_TEMPLATE, filename="", message="File format not allowed.")
#     return render_template_string(HTML_TEMPLATE, filename=None, message=None)

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, render_template_string, jsonify
import os
import werkzeug.utils
import boto3
import logging
import requests
from botocore.exceptions import ClientError

# Setup
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
BUCKET_NAME = 'input-textract-jahnavi'  # Use environment variable or direct assignment

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# HTML template for the app
HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>File Processing with AWS Textract and Polly</title>
  <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body { background: linear-gradient(to right, #6a11cb 0%, #2575fc 100%); color: #fff; }
    .container, .navbar { max-width: 1200px; margin: auto; }
    .card { margin-top: 2rem; background-color: rgba(255, 255, 255, 0.9); }
    .custom-file-label::after { content: "Browse"; }
    .navbar .nav-link { color: #fff !important; }
    section { padding: 2rem 0; }
    .white { color: #000; background-color: rgba(255, 255, 255, 0.8); padding: 20px; border-radius: 8px; margin-bottom: 20px; }
  </style>
</head>
<body>
  <nav class="navbar navbar-expand-lg navbar-dark">
    <a class="navbar-brand" href="#">AWS Services</a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav">
        <li class="nav-item">
          <a class="nav-link" href="#textract">Textract</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#polly">Polly</a>
        </li>
      </ul>
    </div>
  </nav>

  <div class="container">
    <section id="upload">
      <div class="card">
        <div class="card-body">
          <h1 class="card-title mb-4">Upload a File</h1>
          <form action="" method="post" enctype="multipart/form-data">
            <div class="custom-file mb-4">
              <input type="file" class="custom-file-input" name="file" id="file">
              <label class="custom-file-label" for="file">Choose file</label>
            </div>
            <button type="submit" class="btn btn-dark btn-block">Upload</button>
          </form>
          {% if filename %}
            <div class="alert alert-success" role="alert">
              Successfully uploaded: {{ filename }}
            </div>
          {% elif filename == "" %}
            <div class="alert alert-danger" role="alert">
              File format not allowed.
            </div>
          {% endif %}
        </div>
      </div>
    </section>

    <section id="info" class="white">
      <h2>How It Works</h2>
      <p>Transform your documents into lifelike speech with just a few clicks. Our service seamlessly combines the power of AWS Textract and Polly to convert written text into spoken words, making content more accessible for everyone. Here's how you can turn your documents into audio:</p>
      <ol>
        <li><strong>Upload Your Document:</strong> Start by uploading the document you wish to convert. We support a variety of formats including PDF, JPEG, PNG, and more. Please note that the maximum file size allowed is 10MB.</li>
        <li><strong>Text Extraction with AWS Textract:</strong> Upon upload, AWS Textract springs into action, meticulously extracting text from your document. It can accurately identify, read, and interpret text and data, even from forms and tables.</li>
        <li><strong>Text to Speech Conversion with AWS Polly:</strong> The extracted text is then transformed into natural-sounding speech using AWS Polly. This service allows for a high degree of customization, offering dozens of voices across a range of languages.</li>
        <li><strong>Access Your Audio:</strong> Once converted, the audio file is ready for you. You can download the file directly from our site, receive it as an email attachment, or access it through your user dashboard.</li>
      </ol>
    </section>

    <section id="textract" class="white">
      <h2>AWS Textract</h2>
      <p>AWS Textract is a fully managed machine learning service that automatically extracts text, handwriting, and data from scanned documents. Going beyond simple OCR, Textract can identify, read, and interpret text and data, even from forms and tables, making it an essential tool for digital document processing.</p>
    </section>

    <section id="polly" class="white">
      <h2>AWS Polly</h2>
      <p>AWS Polly is a cloud service that turns text into lifelike speech, allowing you to create applications that can talk. Powered by advanced deep learning technologies, Polly offers dozens of lifelike voices across a broad range of languages, enabling the development of new categories of speech-enabled products.</p>
    </section>
  </div>

  <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
  <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
  <script>
    // Update the file label after file select
    $('.custom-file-input').on('change',function(){
      var fileName = $(this).val().split('\\').pop();
      $(this).next('.custom-file-label').addClass("selected").html(fileName);
    })
  </script>
</body>
</html>
"""

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_to_s3(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = file_name
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def get_api_url(api_name, stage_name):
    return f"<p>{api_name, stage_name}</p>"
    # Retrieve the APIs
    region='us-east-1'
    api_gateway_client = boto3.client('apigateway', region_name=region)
    response = api_gateway_client.get_rest_apis()
    # Find the API by name
    api_id = None
    for item in response['items']:
        if item['name'] == api_name:
            api_id = item['id']
            break
    
    if not api_id:
        raise Exception(f"API Gateway '{api_name}' not found.")
 
    # Construct the API URL
    #region = boto3.session.Session().region_name
    api_url = f"https://{api_id}.execute-api.{region}.amazonaws.com/{stage_name}/translate"
    return f"<p>{api_url}</p>"
 
     # Define the JSON body of the request
    json_body = {
    "input_bucket":"input-textract-jahnavi",
    "input_bucket_file":"sampleTextJahnvi.pdf"
    }
 
    try:
        
        # Make the POST request
        response = requests.post(api_url, json=json_body)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Process the response if needed
            return response.json()  # Assuming the response contains JSON data
        else:
            return f"Error: Received status code {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"
 
    return api_url

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')
        if file and allowed_file(file.filename):
            filename = werkzeug.utils.secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            if upload_to_s3(file_path, BUCKET_NAME, filename):
                api_gateway_url =  get_api_url('JahnaviApiGateway', 'prod')
                # if api_gateway_url:
                #     data = {"input_bucket": BUCKET_NAME, "input_bucket_file": filename}
                #     response = requests.post(api_gateway_url + '/textract-polly', json=data)
                #     if response.status_code == 200:
                #         message = f"Successfully uploaded and processed: {filename}"
                #     else:
                #         message = "Error calling API Gateway."
                # else:
                #     message = "API Gateway URL could not be retrieved."
            else:
                message = "Failed to upload to S3."
            return render_template_string(HTML_TEMPLATE, filename=filename, message=message)
        else:
            return render_template_string(HTML_TEMPLATE, filename="", message="File format not allowed.")
    return render_template_string(HTML_TEMPLATE, filename=None, message=None)

if __name__ == '__main__':
    app.run(debug=True)

