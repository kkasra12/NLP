from selenium import webdriver # pip install selenium
from tqdm import tqdm
from pltk import Tokenizer as tok
def getOnePageWords(pageNum,driver,
                    baseUrl="https://dictionary.abadis.ir/fatofa/",
                    headerVariable="pagenumber",
                    file=None):
    driver.get(f"{baseUrl}?{headerVariable}={pageNum}")
    words=driver.find_elements_by_xpath("/html/body/form/section/div[2]/div/div/article/div[3]/a")
    response=[]
    if words==[]:
        print(driver.page_source)
        print(f"Empty wprd list @ {baseUrl}?{headerVariable}={pageNum}")
    for w in words:
        for token in tok.wordTokenizer(w.text)[0]:
            if token.type in ["PERSIAN_WORD"]:
                response.append(token.text)
    return response

if __name__ == '__main__':
    PAGE_MAX_NUM=3243
    options = webdriver.FirefoxOptions()
    # options.add_argument('--headless')
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-dev-shm-usage')
    driver=webdriver.Firefox(executable_path="./geckodriver",options=options)
    # print(getOnePageWords(1,driver))


    dictionaryFile=open("dictionary",'a+')
    print("reading current lists word...")
    allWords=set(dictionaryFile.read().split("\n"))
    lastPageFile=open("numberOfLastPage")
    lastPage=int(lastPageFile.read().replace("\n",""))
    print(f"Starting from page {lastPage}")
    lastPageFile.close()
    for i in tqdm(range(lastPage,PAGE_MAX_NUM)):
        words=getOnePageWords(i,driver)
        if words==[]:
            if input("Continue? [Y/N]").lower()!="y":
                break
            else:
                print(f"retrying for page{i}...")
                words=getOnePageWords(i,driver)
                assert words!=[],"retry failed!!!"
        for w in words:
            if w not in allWords:
                allWords.add(w)
                dictionaryFile.write(f"{w}\n")
        lastPageFile=open("numberOfLastPage",'w')
        lastPageFile.write(str(i))
        lastPageFile.close()
    driver.close()
    dictionaryFile.close()
