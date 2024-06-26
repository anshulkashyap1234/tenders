import requests
from bs4 import BeautifulSoup
import base64
from PIL import Image
from io import BytesIO
import easyocr
import re
from .models import Tender

def save_tenders(data):       
    for key, tender_data in data.items():
            Tender.objects.update_or_create(
                title_ref_no=tender_data['Title and Ref.No./Tender ID'],
                defaults={
                    'e_published_date': tender_data['e-Published Date'],
                    'closing_date': tender_data['Closing Date'],
                    'opening_date': tender_data['Opening Date'],
                    'organisation_chain': tender_data['Organisation Chain'],
                    'tender_location':tender_data['location']
                }
            )
def get_captcha(image_url):
    # Extract base64-encoded data
    encoded_data = image_url.split(',')[1]
    
    # Decode base64 data
    decoded_data = base64.b64decode(encoded_data)
    
    # Open as PIL Image
    image = Image.open(BytesIO(decoded_data))
    
    # Create a new image with white background
    new_image = Image.new("RGB", image.size, "white")
    new_image.paste(image, (0, 0), image)
    
    # Save the processed image
    new_image.save('captcha.jpg')
    
    # Perform OCR using EasyOCR
    reader = easyocr.Reader(['en'])
    result = reader.readtext('captcha.jpg')
    
    # Extract text from OCR result
    captcha = result[0][1] if result else None
    
    if captcha:
        print(f"Detected captcha: {captcha}")
    else:
        captcha = None
    # captcha=input('enter the captcha')
    cleaned_captcha = re.sub(r'[^a-zA-Z0-9]|_\s', '', captcha)
    return cleaned_captcha
 


def main(location,retry=0):
    base_url = 'https://etender.up.nic.in/nicgep/app'
    session = requests.Session()

    cookies = {
        'JSESSIONID': 'AA2AFB982A69CCA5551ECC5669179252.geps2',
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.6',
        'Connection': 'keep-alive',
        'Referer': 'https://etender.up.nic.in/',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-GPC': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        '^sec-ch-ua': '^\\^Not/A)Brand^\\^;v=^\\^8^\\^, ^\\^Chromium^\\^;v=^\\^126^\\^, ^\\^Brave^\\^;v=^\\^126^\\^^',
        'sec-ch-ua-mobile': '?0',
        '^sec-ch-ua-platform': '^\\^Windows^\\^^',
    }

    try:
        # First GET request
        response = session.get(base_url, headers=headers, cookies=cookies)
        cookies.update(response.cookies.get_dict())

        # Parse response
        response = session.get('https://etender.up.nic.in/nicgep/app?page=FrontEndTendersByLocation&service=page', headers=headers,cookies=cookies)
        tag = BeautifulSoup(response.text, 'html.parser')
        hidden_div = tag.find('div', {'id': 'TendersbyLocationhidden'})
        if hidden_div:
            inputs = hidden_div.find_all('input')
            data = {input_tag['name']: input_tag['value'] for input_tag in inputs}
        else:
            raise RuntimeError("Div with id 'TendersbyLocationhidden' not found.")

        # Extract captcha URL and solve captcha
        captcha_url = tag.find('img', {'id': 'captchaImage'})['src']
        captcha = get_captcha(captcha_url)

        # Prepare data for POST request
        data.update({
            'Location': location,
            'captchaText': captcha,
            'submit': 'Submit^'
        })

        # Second POST request
        response = session.post('https://etender.up.nic.in/nicgep/app', headers=headers, data=data, cookies=cookies)

        # Parse response for results
        soup = BeautifulSoup(response.text, 'lxml')
        captcha_img = soup.find('img', {'id': 'captchaImage'})
        if captcha_img is None:
            table_body = soup.find('table', {'class': 'list_table'})
            if table_body:
                extracted_data = {}
                rows = table_body.find_all('tr')
                for row in rows[1:-1]:
                    columns = row.find_all('td')
                    sno = columns[0].get_text(strip=True)
                    epublished_date = columns[1].get_text(strip=True)
                    closing_date = columns[2].get_text(strip=True)
                    opening_date = columns[3].get_text(strip=True)
                    title_ref = columns[4].get_text(strip=True)
                    organisation_chain = columns[5].get_text(strip=True)
                    extracted_data[sno] = {
                        'e-Published Date': epublished_date,
                        'Closing Date': closing_date,
                        'Opening Date': opening_date,
                        'Title and Ref.No./Tender ID': title_ref,
                        'Organisation Chain': organisation_chain,
                        'location':location
                    }
                print(extracted_data)
                save_tenders(extracted_data)
                
            else:
                print("Table with class 'list_table' not found.")
                return -1,{'status':'table not found'}
        else:
            print("Captcha image found unexpectedly.")
            if retry<3:

                main(location)
                retry = retry + 1
            else:
                return -1,{'status':'captcha is wrong after many time retry'}


    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return -1,{'status':'request failed'}

    except Exception as e:
        print(f"An error occurred: {e}")
        return -1,{'status':'error'}

    finally:
        session.close()
        return 1,{'status':'success'}


if __name__ == "__main__":
    main('muzaffarnagar')
