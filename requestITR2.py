import requests

url = "https://www.rad.cvm.gov.br/ENETCONSULTA/frmGerenciaPaginaFRE.aspx"

querystring = {"NumeroSequencialDocumento":"92142","CodigoTipoInstituicao":"2"}

payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"txtLogin\"\r\n\r\n397dwlama\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"txtSenha\"\r\n\r\n19E72C72\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
headers = {
    'authorization': "Basic Mzk3ZHdsYW1hOjE5RTcyQzcy",
    'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
    'cache-control': "no-cache",
    'postman-token': "f94e44b8-48e1-f010-c3f3-5fa3af4a6f84"
    }

response = requests.request("POST", url, data=payload, headers=headers, params=querystring, verify=False)

with open('file.html', 'wb') as f:
    f.write(response.content)

print(response.status_code)