import scrapy

class Spider12(scrapy.Spider):
    name = 'spider12'
    allowed_domains = ['pagina12.com.ar']
    custom_settings = {'FEED_FORMAT': 'json',
                       'FEED_URI': 'resultados_scrapy.json',
                       'DEPTH_LIMIT': 2,
                       'FEED_EXPORT_ENCODING': 'utf-8'}
    start_urls = ['https://www.pagina12.com.ar/secciones/el-pais',
                  'https://www.pagina12.com.ar/secciones/economia',
                  'https://www.pagina12.com.ar/secciones/sociedad',
                  'https://www.pagina12.com.ar/suplementos/cultura-y-espectaculos',
                  'https://www.pagina12.com.ar/secciones/ciencia',
                  'https://www.pagina12.com.ar/secciones/el-mundo',
                  'https://www.pagina12.com.ar/secciones/deportes',
                  'https://www.pagina12.com.ar/secciones/contratapa']

    def parse(self, response):
        featured_el = response.xpath('//div[@class="featured-article__container"]//h2/a/@href').get()
        if featured_el is not None:
            yield response.follow(featured_el, callback=self.parse_new)

        news = response.xpath('//div[@class="article-box__container"]/h2/a/@href').getall()
        for new in news:
            yield response.follow(new, callback=self.parse_new)

        next_page = 'https://www.pagina12.com.ar{}'.format(
            response.xpath('//a[@class="pagination-btn-next"]/@href').get())
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_new(self, response):
        title = response.xpath('//div[@class="article-titles"]//h1/text()').get()
        body = ' '.join(response.xpath('//div[@class="article-text"]/p/text()').getall())
        section = response.xpath('//div[@class= "suplement"]/a/text()').get()
        yield {'section': section,
               'url': response.url,
               'title': title,
               'body': body}
