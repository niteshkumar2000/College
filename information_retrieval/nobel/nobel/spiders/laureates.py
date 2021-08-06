import scrapy


# helper to generate single person data
def make_row(year, category, winners_list, link_list):
    data = []
    for winner, link in zip(winners_list, link_list):
        data.append({
            "year": year[0].strip(),
            "category": category,
            "name": winner,
            "link": link
        })
    return data


class LaureatesSpider(scrapy.Spider):
    name = 'laureates'
    start_urls = ['https://en.wikipedia.org/wiki/List_of_Nobel_laureates']

    def parse(self, response):
        rows = response.xpath('..//table[1]//tbody//tr')
        del rows[0]
        for row in rows:
            year = row.xpath("td[1]//text()").extract()
            physics_winners = row.xpath("td[2]//a//text()").extract()
            physics_winners_wiki = row.xpath("td[2]//a//@href").extract()
            chemistry_winners = row.xpath("td[3]//a//text()").extract()
            chemistry_winners_wiki = row.xpath("td[3]//a//@href").extract()
            medicine_winners = row.xpath("td[4]//a//text()").extract()
            medicine_winners_wiki = row.xpath("td[4]//a//@href").extract()
            literature_winners = row.xpath("td[5]//a//text()").extract()
            literature_winners_wiki = row.xpath("td[5]//a//@href").extract()
            peace_winners = row.xpath("td[6]//a//text()").extract()
            peace_winners_wiki = row.xpath("td[6]//a//@href").extract()
            economics_winners = row.xpath("td[7]//a//text()").extract()
            economics_winners_wiki = row.xpath("td[7]//a//@href").extract()
            if not year:
                break
            data_list = [make_row(year, "physics", physics_winners, physics_winners_wiki),
                         make_row(year, "chemistry", chemistry_winners, chemistry_winners_wiki),
                         make_row(year, "medicine", medicine_winners, medicine_winners_wiki),
                         make_row(year, "literature", literature_winners, literature_winners_wiki),
                         make_row(year, "peace", peace_winners, peace_winners_wiki),
                         make_row(year, "economics", economics_winners, economics_winners_wiki)
                         ]
            for category_data in data_list:
                for data in category_data:
                    yield data
