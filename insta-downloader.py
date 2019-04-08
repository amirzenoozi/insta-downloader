__author__ = "Amirhossein Douzendeh Zenoozi"
__license__ = "MIT"
__version__ = "1.0"


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import urllib.request as req
import requests
import shutil
import time
import re


def checkUrlFormat( url ):
    pattern = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    if( pattern.match( url ) ):
        return True
    else:
        return False



def downloadImageFile( imageUrl, targetName ):
    opener = req.build_opener()
    opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    req.install_opener(opener)
    req.urlretrieve( imageUrl, targetName+'.jpg')
    return True;



def downloadVideoFile( imageUrl, targetName ):
    opener = req.build_opener()
    opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    req.install_opener(opener)
    req.urlretrieve( imageUrl, targetName+'.mp4')
    return True;



def exportPageSourceAsFile( driver, fileName = 'PageSource' ):
    file = open( fileName+'.html', 'w', encoding='utf-8')
    #file.write( driver.page_source )
    file.write( driver.get_attribute('innerHTML') )
    file.close()



def exportAltDescriptionOfImage( driver ):
    _SELECTOR_ = '//main/div/div/article/header/following-sibling::div[1]/div/div/div/img'
    _ELEMENT_ = driver.find_element_by_xpath( _SELECTOR_ )
    return _ELEMENT_.get_attribute('alt')



def exportTitlePage( driver ):
    _SELECTOR_ = '//main/div/div/article/header/div/following-sibling::div[1]//a'
    _ELEMENT_ = driver.find_element_by_xpath( _SELECTOR_ )
    return _ELEMENT_.text


def postGallery( driver ):
    _MULTI_SELECTOR_ = '//main/div/div/article/header/following-sibling::div[1]/div/div/div/div/following-sibling::div[1]//ul'
    _FIRST_BTN_SELECTOR_ = '//main/div/div/article/header/following-sibling::div[1]/div/div/div/div/following-sibling::div[1]//button[1]'
    _SECOND_BTN_SELECTOR_ = '//main/div/div/article/header/following-sibling::div[1]/div/div/div/div/following-sibling::div[1]//button[2]'
    _MULTI_LIST_ELEMENT_ = driver.find_element_by_xpath( _MULTI_SELECTOR_ )
    _ITEMS_COUNT_ = len( _MULTI_LIST_ELEMENT_.find_elements_by_xpath(".//li") )
    _PAGE_TITLE_ = exportTitlePage( driver )
    try: 
        for i in range(0,_ITEMS_COUNT_):
            _ITEM_ = ''
            if( i == 2 ):
                driver.find_element_by_xpath( _FIRST_BTN_SELECTOR_ ).click()
            elif( i > 2 and i < _ITEMS_COUNT_  ):
                driver.find_element_by_xpath( _SECOND_BTN_SELECTOR_ ).click()
            _ITEM_ = _MULTI_LIST_ELEMENT_.find_elements_by_xpath(".//li")[i]
            _isImageItem_ = False
            _isVideoItem_ = False

            try:
                _VID_SRC_ = _ITEM_.find_elements_by_xpath("//div/video[@preload='none']")[i].get_attribute('src')
                _isVideoItem_ = True
            except NoSuchElementException:
                _isVideoItem_ = False
            except IndexError:
                _isVideoItem_ = False
                print('List Index')

            try:
                _IMG_SRC_ = _ITEM_.find_elements_by_xpath("//div/img[@decoding='auto']")[0].get_attribute('src')
                _isImageItem_ = True
            except NoSuchElementException:
                _isImageItem_ = False
            except IndexError:
                _isImageItem_ = False
                print('List Index')


            if( _isVideoItem_ ):
                #print( _VID_SRC_ )
                downloadVideoFile( _VID_SRC_, 'vid_' + _PAGE_TITLE_ + '_' + str(int(time.time())) )
            elif( _isImageItem_ and not _isVideoItem_ ):
                #print( _IMG_SRC_ )
                downloadImageFile( _IMG_SRC_, 'img_' + _PAGE_TITLE_ + '_' + str(int(time.time())) )
            else:
                print('not Supportable Item')

    except NoSuchElementException:
        print('Can\'t Find Gallery List')



def InstagramPostTypeDetection( driver ):
    _IMG_SELECTOR_ = '//main/div/div/article/header/following-sibling::div[1]/div/div/div/img'
    _PAGE_TITLE_ = exportTitlePage( driver )
    _isImage_ = False
    try:
        _IMG_ELEMENT_ = driver.find_element_by_xpath( _IMG_SELECTOR_ )
        _isImage_ = True
    except NoSuchElementException:
        _isImage_ = False

    
    _VID_SELECTOR_ = '//main/div/div/article/header/following-sibling::div[1]/div/div/div/video'
    _isVideo_ = False
    try:
        _VID_ELEMENT_ = driver.find_element_by_xpath( _VID_SELECTOR_ )
        _isVideo_ = True
    except NoSuchElementException:
        _isVideo_ = False

    _MULTI_SELECTOR_ = '//main/div/div/article/header/following-sibling::div[1]/div/div/div/div/following-sibling::div[1]//ul'
    _isMulti_ = False
    try:
        _MULTI_ELEMENT_ = driver.find_element_by_xpath( _MULTI_SELECTOR_ )
        _isMulti_ = True
    except NoSuchElementException:
        _isMulti_ = False
    
    if( _isImage_ ):
        print('This is Singular Image')
        downloadImageFile( _IMG_ELEMENT_.get_attribute('src'), 'img_' + _PAGE_TITLE_ + '_' + str(int(time.time())) )
    elif( _isVideo_ ):
        print('This is Singular Video')
        downloadVideoFile( _VID_ELEMENT_.get_attribute('src'), 'vid_' + _PAGE_TITLE_ + '_' + str(int(time.time())) )
    elif( _isMulti_ ):
        print('This is Gallery')
        postGallery( driver )



def openSeleniumBrowser( url ):
    _DRIVER_PATH_ = r'C:chromedriver.exe'
    _OPT_ = webdriver.ChromeOptions()
    _OPT_.add_argument('headless')
    _DRIVER_ = webdriver.Chrome( _DRIVER_PATH_, options = _OPT_ )
    _DRIVER_.get( url )
    InstagramPostTypeDetection( _DRIVER_ )
    _DRIVER_.close()
    _DRIVER_.quit()


    
def init():
    _TARGET_ = ''
    while( True ):
        _TARGET_ = input('Please Enter Instagram Post URL: ')
        if( _TARGET_ == 'end' ):
            break
        else:
            if( checkUrlFormat( _TARGET_ ) ):
                openSeleniumBrowser( _TARGET_ )
                print('\n')
            else:
                print('\n')
                print('========================')
                print('Please Inter Valid URL!!')
                print('========================')
                print('\n')

if __name__ == '__main__':
    init()
else:
    print(__name__)
