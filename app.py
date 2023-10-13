import os
import requests


API_KEY = "kebbsz93@gmail.com_00744ef30a5799fdf1f967b1dd93db24a074a628f7f326e7b38ff02bf1f489afef14760d"

BASE_URL = "https://api.pdf.co/v1"

SourceFile = ".\\Coding_Challange_2.pdf"

Pages = ""

Password = ""

DestinationFile = ".\\result.html"

PlainHtml = False

ColumnLayout = False


def main(args=None):
    uploadedFileUrl = uploadFile(SourceFile)
    if (uploadedFileUrl != None):
        convertPdfToHtml(uploadedFileUrl, DestinationFile)


def convertPdfToHtml(uploadedFileUrl, destinationFile):
    """Converts PDF To Html using PDF.co Web API"""

    parameters = {}
    parameters["name"] = os.path.basename(destinationFile)
    parameters["password"] = Password
    parameters["pages"] = Pages
    parameters["simple"] = PlainHtml
    parameters["columns"] = ColumnLayout
    parameters["url"] = uploadedFileUrl

    # Prepare URL for 'PDF To Html' API request
    url = "{}/pdf/convert/to/html".format(BASE_URL)

    response = requests.post(url, data=parameters, headers={
        "x-api-key": API_KEY})
    if (response.status_code == 200):
        json = response.json()

        if json["error"] == False:
            resultFileUrl = json["url"]
            r = requests.get(resultFileUrl, stream=True)
            if (r.status_code == 200):
                with open(destinationFile, 'wb') as file:
                    for chunk in r:
                        file.write(chunk)
                print(f"Result file saved as \"{destinationFile}\" file.")
            else:
                print(f"Request error: {
                      response.status_code} {response.reason}")
        else:
            print(json["message"])
    else:
        print(f"Request error: {response.status_code} {response.reason}")


def uploadFile(fileName):
    """Uploads file to the cloud"""
    url = "{}/file/upload/get-presigned-url?contenttype=application/octet-stream&name={}".format(
        BASE_URL, os.path.basename(fileName))

    response = requests.get(url, headers={"x-api-key": API_KEY})
    if (response.status_code == 200):
        json = response.json()

        if json["error"] == False:
            uploadUrl = json["presignedUrl"]
            uploadedFileUrl = json["url"]

            with open(fileName, 'rb') as file:
                requests.put(uploadUrl, data=file, headers={
                    "x-api-key": API_KEY, "content-type": "application/octet-stream"})

            return uploadedFileUrl
        else:
            print(json["message"])
    else:
        print(f"Request error: {response.status_code} {response.reason}")

    return None


if __name__ == '__main__':
    main()
