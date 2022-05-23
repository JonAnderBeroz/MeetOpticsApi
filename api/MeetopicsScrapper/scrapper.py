from bs4 import BeautifulSoup
import requests
import json

OPTOSIGMA_WEB = 'https://www.optosigma.com/eu_en/optics/lenses/spherical-lenses/plano-convex-spherical-lenses/spherical-lens-bk7-plano-convex-uncoated-SLB-P.html'
THORLABS_WEB = ' http://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=112'

# Gets web content of the given url
def getWebContent(url):
    return requests.get(url).content

# Gets soup for the given web content
def getSoup(webContent):
    return BeautifulSoup(webContent, 'html.parser')

# Get the soup of an specific lense 
def getOptoSigmaLenseSoup(lense):
    lenseDetailUrl = lense.find('td').find('a').get('href')
    return getSoup(getWebContent(lenseDetailUrl))

# Get details of an specific lense
def getOptoSigmaLenseDetails(lenseSoup):    
    lenseDetailTable = lenseSoup.find('table', id='product-attribute-specs-table')
    return lenseDetailTable.find_all('td')

# Gets the price of an specific lense
def getOptoSigmaLensePrice(lense, lenseSoup):
    dataId = lense.get('data-id')
    return lenseSoup.find('span', id='product-price-'+ dataId).get('data-price-amount')

# Generates json from the data
def generateJson(data):
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

# Generates soup for OptoSigma site
def getOptoSigmaSoup():
    webContent = getWebContent(OPTOSIGMA_WEB)
    return getSoup(webContent)

# Generates soup for ThorLabs site
def getThorLabsSoup():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0', 'authorization': 'SAPISIDHASH d6479444928a28da1b55b56b3a90c4bd402baa68content-length: 830', 'cookie': 'CONSENT=YES+srp.gws-20210707-0-RC1.es+FX+091; __Secure-3PSID=Jgi_8eEooMIm_ttjMN9A_As_Z3NAMIz_5SYf5O_et3eJOrBgxSQndh6Qo5Gdj-wwA2ogZg.; __Secure-3PAPISID=09m7OBlwRsVv5kGF/AMqKX1FXYd4EYMfEZ; 1P_JAR=2022-05-19-09; NID=511=AZ4eooA6mDGEGZId-tF1FSZFIZwmTPJHUcBz7ogvMJGcxJXmN86YiqmhnPJZZEg9GecxF0xCYpmeOwsH4OqPw1PC_46J3GEOFffNDdc5U3_kbKZkPmndZgSWJLWSMG_BLH1zcWYg4igm7bo4ugoXdMrpeSBMlgDwN-BXERCvpVaC3cQm7kMH3BNTa26YvuY0hpQQQu_-ixdmLPE4OZbtJZTN9UxnPD-WZbSDbd8-ogCC3SkOX7zMOPzRkg; __Secure-3PSIDCC=AJi4QfHszcENZv1FlAyc1nFZmk0TA6gMbs7otPvZARNRsgh5v8cY14F__nBghZ3FlNcPi28mFQ'}
    webContent = requests.get(THORLABS_WEB, headers=headers)
    print(webContent)
    return getSoup(webContent.content.decode())

# Generates lense data for OptoSigma site 
def getOptoSigmaData():
    lenseTable = getOptoSigmaSoup().find('table', id='super-product-table').find('tbody')
    lenseData = {}
    i = 0
    for lense in lenseTable.find_all('tr'):
        lenseId = lense.find('td').find('span').string.strip()
        lenseDetails = {}
        lenseSoup = getOptoSigmaLenseSoup(lense)
        lensePrice = getOptoSigmaLensePrice(lense, lenseSoup)
        lenseDetails['provider'] = 'OptoSigma'
        lenseDetails['price'] = lensePrice
        for detail in getOptoSigmaLenseDetails(lenseSoup):
            lenseDetails[detail.get('data-th').strip().lower().replace('φd', '').strip().replace(' ', '_')] = detail.text.replace('φ', '').replace('mm', '').replace('kgs', '').strip()
        lenseData[lenseId] = lenseDetails
        print(i)
        i+=1
    return lenseData
# Generates lense data for ThorLab site
def getThorLabsData():
    print(getThorLabsSoup().prettify())

