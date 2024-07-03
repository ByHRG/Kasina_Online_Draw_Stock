import requests
from bs4 import BeautifulSoup


class KASINADRAW:
    def __init__(self):
        self.url = "https://www.kasina.co.kr/goods/goods_entry_view.php?goodsNo="

    def url_setting(self, url):
        return url.split("&")[0].split("goodsNo=")[-1]

    def run(self, product_code):
        if "kasina" in product_code:
            product_code = self.url_setting(product_code)
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Cookie": "넷퍼넬 숨김",
        }
        req = requests.get(self.url + product_code, verify=False, headers=header)
        soup = BeautifulSoup(req.text, "html.parser")
        output = {
            "Name": soup.find("div", {"class": "goods-header"})
            .find("div", {"class": "tit"})
            .text.strip()
            .replace("\n", " "),
            "Image": soup.find("div", {"class": "swiper-slide"}).find("img")["src"],
            "Price": soup.find("input", {"name": "set_goods_price"})["value"],
            "Url": "https://www.kasina.co.kr/goods/goods_view.php?goodsNo="
            + str(product_code),
            "AllStock": 0,
            "Stock": {},
        }
        data = soup.find("li", {"class": "drawOption"}).findAll("option")
        del data[0]
        header["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"

        for i in data:
            post_data = f"mode=option_select&optionVal%5B%5D={i.text}&optionKey=0&goodsNo={str(product_code)}&mileageFl=+c"
            req = requests.post(
                "https://www.kasina.co.kr/goods/goods_ps.php",
                data=post_data,
                headers=header,
                verify=False,
            )
            data = {i.text: {}}
            for j in range(len(req.json()["nextOption"])):
                output["AllStock"] += int(req.json()["stockCnt"][j])
                data[i.text].update(
                    {req.json()["nextOption"][j]: req.json()["stockCnt"][j]}
                )
            output["Stock"].update(data)
        # for i in output['Stock']:

        return output



url = 'https://www.kasina.co.kr/goods/goods_entry_view.php?goodsNo=1242687580&sno=173'

print(KASINADRAW().run(url))
