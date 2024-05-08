import requests
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.vps_buy_models import VpsBuyModel, VpsTemplateModel
import re

req_session = requests.Session()
cf_token = None
api_post_data = None


def get_data_req(template_data: VpsBuyModel):
    global api_post_data
    api_post_data = template_data


def login_whmcs():
    global req_session, cf_token, api_post_data
    req_session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    })
    login_response = req_session.get(api_post_data.login_address, verify=False)
    html_token = re.findall("csrfToken = '(.+?)'", login_response.text)
    if html_token:
        cf_token = html_token[0]
        req_session.headers['referer'] = api_post_data.login_address
        req_session.headers['content-type'] = 'application/x-www-form-urlencoded'
        login_data = {
            'token': cf_token,
            'username': api_post_data.template_username,
            'password': api_post_data.template_passwd,
        }
        login_post_response = req_session.post(api_post_data.login_address, data=login_data, verify=False)
        if 'clientarea' in login_post_response.url:
            return {"status": "success", "data": "login success"}
        else:
            return {"status": "fail", "data": "login fail"}
    else:
        raise HTTPException(status_code=404, detail="CF_token not found")


def web_login(template_data: VpsBuyModel):
    get_data_req(template_data)
    login_status = login_whmcs()
    return login_status
