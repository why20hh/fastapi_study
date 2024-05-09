import datetime
from sqlalchemy.orm import Session
from models.vps_goods_scanning import VpsGoodsScanningModels
from fastapi import HTTPException
from datetime import datetime
import re
import requests
from utils.middleware import logger
from urllib3.exceptions import InsecureRequestWarning
import warnings
from urllib.parse import urlparse

warnings.filterwarnings('ignore', category=InsecureRequestWarning)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}


def scanning_goods(vps_goods_name_url):
    response = requests.get(vps_goods_name_url, headers=headers, verify=False, timeout=30)
    if response.status_code == 200:
        get_response_result = re.findall(r"document\.write\('([^']*)'\);?", response.text)
        if get_response_result:
            get_response_result = get_response_result[0]
            print(get_response_result)
            return get_response_result
        else:
            print(response.text)
            logger.info('接口返回内容有误')
            return False
    else:
        logger.info('获取接口内容失败')
        return False


def scanning_goods_curd(db: Session, scan_url: str, num_of_scan: int):
    for i in range(num_of_scan):
        vps_goods_name_url = scan_url + f'/feeds/productsinfo.php?pid={i}&get=name'
        vps_goods_name_result = scanning_goods(vps_goods_name_url)
        if vps_goods_name_result and vps_goods_name_result != 'Product ID Not Found':
            vps_goods_description_result = scanning_goods(
                scan_url + f'/feeds/productsinfo.php?pid={i}&get=description')
            if vps_goods_description_result:
                vps_goods_description_result = re.sub(r'<[^>]+>', '', vps_goods_description_result)
                vps_goods_description_result = re.sub(r'&[a-zA-Z]+;', '', vps_goods_description_result)
                vps_price_monthly_result = scanning_goods(
                    scan_url + f'/feeds/productsinfo.php?pid={i}&get=price&billingcycle=monthly')
                vps_price_quarterly_result = scanning_goods(
                    scan_url + f'/feeds/productsinfo.php?pid={i}&get=price&billingcycle=quarterly')
                vps_price_annually_result = scanning_goods(
                    scan_url + f'/feeds/productsinfo.php?pid={i}&get=price&billingcycle=annually')
                # 先查询是否存在:
                vps_goods_select = db.query(VpsGoodsScanningModels).filter(
                    VpsGoodsScanningModels.vps_goods_name == vps_goods_name_result).first()
                if vps_goods_select:
                    try:
                        vps_goods_select.vps_goods_name = vps_goods_name_result,
                        vps_goods_select.vps_goods_description = vps_goods_description_result,
                        vps_goods_select.vps_price_monthly = vps_price_monthly_result,
                        vps_goods_select.vps_price_quarterly = vps_price_quarterly_result,
                        vps_goods_select.vps_price_annually = vps_price_annually_result,
                        vps_goods_select.vps_service_name = urlparse(scan_url).netloc
                        vps_goods_select.vps_buy_link = scan_url + f'/cart.php?a=add&pid={i}'
                        vps_goods_select.vps_data_last_edit_time = datetime.now()
                        db.commit()
                        db.refresh(vps_goods_select)
                    except Exception as e:
                        return {"status": "error", "message": str(e)}
                else:
                    add_vps_goods_scan_data = VpsGoodsScanningModels(
                        vps_goods_name=vps_goods_name_result,
                        vps_goods_description=vps_goods_description_result,
                        vps_price_monthly=vps_price_monthly_result,
                        vps_price_quarterly=vps_price_quarterly_result,
                        vps_price_annually=vps_price_annually_result,
                        vps_buy_link=scan_url + f'/cart.php?a=add&pid={i}',
                        vps_service_name=urlparse(scan_url).netloc
                    )
                    db.add(add_vps_goods_scan_data)
                    db.commit()
                    db.refresh(add_vps_goods_scan_data)
            else:
                break
