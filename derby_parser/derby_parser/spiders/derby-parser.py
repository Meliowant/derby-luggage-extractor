import scrapy
import re
from collections import namedtuple

Luggage = namedtuple("Luggage", ["name", "int_code", "price", "specs"])

Specs = namedtuple("Specs", [
    "width", "length", "height", "volume", "wheels", "weight", "features",
    "meterial", "warranty",
])

class DerbyParser(scrapy.Spider):
    name = "luggage-parser"
    item_urls = []
    items = []

    def start_requests(self):
        urls = [
            "https://derby.ua/v-dorogu/chemodany/ruchnaja-klad/",
            "https://derby.ua/v-dorogu/chemodany/ruchnaja-klad/page-2",
            "https://derby.ua/v-dorogu/chemodany/ruchnaja-klad/page-3",
            "https://derby.ua/v-dorogu/chemodany/ruchnaja-klad/page-4",
            "https://derby.ua/v-dorogu/chemodany/ruchnaja-klad/page-5",
            "https://derby.ua/v-dorogu/chemodany/ruchnaja-klad/page-6",
            "https://derby.ua/v-dorogu/chemodany/ruchnaja-klad/page-7",
            "https://derby.ua/v-dorogu/chemodany/ruchnaja-klad/page-8",
            "https://derby.ua/v-dorogu/chemodany/ruchnaja-klad/page-9",
            "https://derby.ua/v-dorogu/chemodany/ruchnaja-klad/page-10",
            "https://derby.ua/v-dorogu/chemodany/ruchnaja-klad/page-11",
            "https://derby.ua/v-dorogu/chemodany/ruchnaja-klad/page-12",
            "https://derby.ua/v-dorogu/chemodany/ruchnaja-klad/page-13",
            "https://derby.ua/v-dorogu/chemodany/ruchnaja-klad/page-14",
            "https://derby.ua/v-dorogu/chemodany/ruchnaja-klad/page-15",
            "https://derby.ua/v-dorogu/chemodany/ruchnaja-klad/page-16",
            "https://derby.ua/v-dorogu/chemodany/ruchnaja-klad/page-17",
            "https://derby.ua/v-dorogu/chemodany/ruchnaja-klad/page-18",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_page)

        for url in self.item_urls:
            self.items.append(
                scrapy.Request(url=url, callback=self.parse_item)
            )

        # TODO Write everyting to CSV


    def parse_page(self, response):
        for item in response.xpath("a[@class='product-item']"):
            self.item_urls.append(item.xpath("@href").get())

    def parse_item(self, response):
        title = response.css("h1::text").get()

        parsed = re.search("\d+", response.css("h1 span::text").get())
        int_code = parsed[0] if parsed else ''

        price = response.css("div.productMainInfo span.price-new")
        if not discount_price:
            price = response.css("div.productMainInfo span.priceUAH")
        price = discount_price.css("::text").get()
        price = float(price)

        specs = parse_specs(response)
        # TODO Create complete luggage item
        luggage = Luggage(
            name=title, int_code=int_code, price=price, specs=specs
        )
        return luggage


    def parse_specs(response):
        width = 0
        length = 0
        height = 0
        weight = 0
        warranty = ""
        wheels_no = 0
        origin = ""
        material = ""
        volume_range = ""
        features = ""
        scope = ""
        size = ""
        volume = 0

        for specs in response.xpath("//div[@class='productSpecification']//li"):
            header = specs.xpath("span/text()")[0].extract().strip()
            data = specs.xpath("span/text()")[1].extract()
            print(f"-> {header}\n--> {data}")

            if header == "Розміри (см)":
                width, length, height = get_luggage_dimension(data)

            if header == "Вага (кг)":
                pass

            if header == "Гарантія":
                pass

            if header == "Кількість колес":
                pass

            if header == "Країна бренду":
                pass

            if header == "Матеріал":
                pass

            if header == "Об'єм (літрів)":
                pass

            if header == "Оснащення":
                pass

            if header == "Призначення":
                pass

            if header == "Розмір":
                pass

            if  header == "Об'єм (л)":
                pass

        specs = Specs(
            width=width, length=length, height=height, weigth=weigth,
            warranty=warranty, wheels=wheels, origin=origin, material=material,
            volume_range=volume_range, features=features, scope=scope,
            size=size, volume=volume
        )
        return specs
