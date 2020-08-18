import requests
from bs4 import BeautifulSoup
from urllib import parse
import re

month = 4
year = 1912


def CNTS(digital_title, digital_sub_title, digital_date, subtitle):
    # -------------CNTS-XXXXXXXXXXX----------------------
    url = "https://www.nl.go.kr/NL/contents/search.do?resultType=&pageNum=1&pageSize=30&order=&sort=&srchTarget=total&kwd=" + parse.quote(digital_title)+"&systemType=" + parse.quote('온라인자료')+"&lnbTypeName=&category=" + parse.quote(
        '잡지/학술지')+"&hanjaFlag=&reSrchFlag=&licYn=&kdcName1s=&manageName=&langName=&ipubYear="+str(year)+"&pubyearName=&seShelfCode=&detailSearch=&seriesName=&mediaCode=&offerDbcode2s=&f1=&v1=&f2=&v2=&f3=&v3=&f4=&v4=&and1=&and2=&and3=&and4=&and5=&and6=&and7=&and8=&and9=&and10=&and11=&and12=&isbnOp=&isbnCode=&guCode2=&guCode3=&guCode4=&guCode5=&guCode6=&guCode7=&guCode8=&guCode11=&gu2=&gu7=&gu8=&gu9=&gu10=&gu12=&gu13=&gu14=&gu15=&gu16=&subject=&sYear=&eYear=&sRegDate=&eRegDate=&typeCode=&acConNo=&acConNoSubject=&infoTxt="

    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    total_num = (soup.find_all('span', class_='txt_blue'))[2].get_text()
    total_num = total_num.replace(",", "")
    # print('url : ' + url)

    url = f"https://www.nl.go.kr/NL/contents/search.do?resultType=&pageNum=1&pageSize={total_num}&order=&sort=&srchTarget=total&kwd=" + parse.quote(digital_title)+"&systemType=" + parse.quote('온라인자료')+"&lnbTypeName=&category=" + parse.quote(
        '잡지/학술지')+"&hanjaFlag=&reSrchFlag=&licYn=&kdcName1s=&manageName=&langName=&ipubYear="+str(year)+"&pubyearName=&seShelfCode=&detailSearch=&seriesName=&mediaCode=&offerDbcode2s=&f1=&v1=&f2=&v2=&f3=&v3=&f4=&v4=&and1=&and2=&and3=&and4=&and5=&and6=&and7=&and8=&and9=&and10=&and11=&and12=&isbnOp=&isbnCode=&guCode2=&guCode3=&guCode4=&guCode5=&guCode6=&guCode7=&guCode8=&guCode11=&gu2=&gu7=&gu8=&gu9=&gu10=&gu12=&gu13=&gu14=&gu15=&gu16=&subject=&sYear=&eYear=&sRegDate=&eRegDate=&typeCode=&acConNo=&acConNoSubject=&infoTxt="
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    a = (soup.select('div.row'))
    for index in a:
        b = (index.select('a.btn_layer.detail_btn_layer'))[0]
        control_num = (re.findall(r'(?<=\=).+?(?=\&)', b['href']))[0]
        sub_url = f"https://www.nl.go.kr/NL/search/mods_view.do?contentsId="+control_num
        urltemp = sub_url
        req_sub = requests.get(urltemp)
        # print(urltemp)
        html_sub = req_sub.text
        sub = BeautifulSoup(html_sub, 'lxml')
        # print(sub)
        title = (sub.find('title').get_text(strip=True))
        date = (sub.find('dateissued')).get_text(strip=True)
        print(title+"   "+date)
        if subtitle:
            # print("부제 넘어감")
            try:
                subtitle_ = (sub.find('subtitle')).get_text(strip=True)
                if date == digital_date and (digital_title+" : "+digital_sub_title) == (title+" : "+subtitle_):
                    print(digital_title + " / " + title + " / "+subtitle_)
                    return control_num
            except:
                print('.')

        else:
            if date == digital_date and title == digital_title:
                return control_num
        # 못찾음
    return 0


f = open("result_"+str(year)+"_"+str(month) + ".txt", 'a')
# --------------------조선총독뭐시기---------------------
url = 'https://www.nl.go.kr/NL/contents/N20302010000.do?searchType=month&schM=day_list&page=1&pageSize=200&searchYear=1912&searchMonth=4'
req = requests.get(url)
print("digital_url:"+url)
html = req.text
soup_digital = BeautifulSoup(html, 'html.parser')
total_num = soup_digital.find('span', {'class': 'total_num'}).get_text()
total_num = total_num.replace(",", "")
url = f'https://www.nl.go.kr/NL/contents/N20302010000.do?searchType=month&schM=day_list&page=1&pageSize=200&searchYear=1912&searchMonth=4'
req = requests.get(url)
html = req.text
soup_digital = BeautifulSoup(html, 'html.parser')
digital_list = soup_digital.find('ul', class_='ucsrch8_list')
digital_item = digital_list.find_all('li', class_='ucsrch8_item')
i = 45
# print(digital_item[i])
# print(len(digital_item[i].select('p.paper_info')))
#b = (digital_item[i].select('p.paper_info'))
# print(b)
# print('gisaId'+str(i))

digital_title = digital_item[i].find(
    'strong', {'class': 'title'}).get_text()  # 제목
digital_title = digital_title.strip()
digital_control_num = (digital_list.find(
    'input', {'name': 'gisaId'+str(i)}).get('value'))  # 제어번호
digital_date = (re.findall(
    r'(?<=\_).+?(?=\_)', digital_control_num))[0]  # 날짜
digital_date = digital_date.strip()
try:
    digital_writer = (digital_item[i].find(
        'p', {'class': 'paper_info'}).span).get_text()
except:  # 호외
    digital_writer = '0'
subtitle = 0
if '작성자 ' in digital_writer:
    digital_writer = digital_writer.replace("작성자 : ", "")  # 작성자
    print("digital_title : " + digital_title +
          " /digital_date : " + digital_date)
    control_num_ = CNTS(digital_title, ' ',
                        digital_date, subtitle)
    subtitle = 0
elif '부제' in digital_writer:
    digital_writer = digital_writer.replace("부제 : ", "")  # 작성자
    digital_sub_title = digital_writer
    print("digital_title : " + digital_title + " /digital_sub : " +
          digital_sub_title + " /digital_date : " + digital_date)
    subtitle = 1
    control_num_ = CNTS(digital_title, digital_sub_title,
                        digital_date, subtitle)
    # print("부제있음!")

else:
    print("digital_title : " + digital_title +
          " /digital_date : " + digital_date)
    subtitle = 0
    control_num_ = CNTS(digital_title, ' ',
                        digital_date, subtitle)
print(control_num_)
print(digital_control_num, "    ", control_num_)
if subtitle:
    data = digital_sub_title + "/" + digital_date + "/" +\
        digital_control_num + "/" + control_num_ + "\n"
else:
    data = digital_title + "/" + digital_date + "/" +\
        digital_control_num + "/" + control_num_ + "\n"

f.write(data)

i += 1
f.close()
