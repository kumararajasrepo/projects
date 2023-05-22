import requests
from config_reader.config import Config
from bs4 import BeautifulSoup
from gnews.article import Article
from logger.log import Log

class Consumer:
    def __init__(self,name):
        self.name=name
    
    def news_compile(self):
        articles = []        
        try:   
            config=Config("configuration")
            config_data=config.get_config_data()         
            response = requests.get(config_data["news_url"])            
            soup = BeautifulSoup(response.text, 'html.parser')
            article_elements = soup.find_all('article')
            article_images=soup.find_all('figure')
            arlength=len(article_elements)
            for arindex in range(arlength):
                article=article_elements[arindex]
                headline_element = article.find('h3', class_=config_data["article_class"])                                      
                if headline_element:                    
                    headline = headline_element.text                    
                    link = config_data["article_link"] + article.find('a')['href']
                    if len(article_images) > arindex:
                        aimage=article_images[arindex]
                        if aimage is not None:
                            aimage_element = aimage.find('img', class_=config_data["image_class"]) 
                            aimagesrc=aimage_element.get('src')
                    articles.append(Article(f"{headline}",f"{link}",f"{aimagesrc}"))
                    
            return articles
        except Exception as e:
            log=Log("Logging")
            log.write(e)              