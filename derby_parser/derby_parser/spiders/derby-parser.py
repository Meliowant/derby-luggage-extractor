import scrapy
import re
from collections import namedtuple

Luggage = namedtuple("Luggage", ["name", "int_code", "price", "specs"])

Specs = namedtuple("Specs", [
    "width", "length", "height", "volume", "wheels", "weight", "features",
    "material", "warranty", "origin", "volume_range", "scope", "size"
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
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        for item in response.xpath("//a[@class='product-item']"):
            yield scrapy.Request(
                url=item.xpath("@href").get(), callback=self.parse_item
            )

    def parse_item(self, response):
        title = response.css("h1::text").get()

        parsed = re.search("\d+", response.css("h1 span::text").get())
        int_code = parsed[0] if parsed else ''

        price = response.css("div.productMainInfo span.price-new")
        if not price:
            price = response.css("div.productMainInfo span.priceUAH")
        price = price.css("::text").get()
        price = float(price) if price else price

        specs = self.parse_specs(response)
        luggage = Luggage(
            name=title, int_code=int_code, price=price, specs=specs
        )
        yield {
            "title": title,
            "int_code": int_code,
            "price": price,
            "width": specs.width,
            "length": specs.length,
            "height": specs.height,
            "weight": specs.weight,
            "warranty": specs.warranty,
            "wheels no": specs.wheels,
            "origin": specs.origin,
            "material": specs.material,
            "volume range": specs.volume_range,
            "features": specs.features,
            "scope": specs.scope,
            "size": specs.size,
            "volume": specs.volume,
        }


    def parse_specs(self, response):
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
            # print(f"-> {header}\n--> {data}")

            if header == "Розміри (см)":
                width, length, height = self.get_luggage_dimension(data)

            if header == "Вага (кг)":
                weight = data

            if header == "Гарантія":
                warranty = data

            if header == "Кількість колес":
                wheels_no = data

            if header == "Країна бренду":
                origin = data

            if header == "Матеріал":
                material = data

            if header == "Об'єм (літрів)":
                volume_range = data

            if header == "Оснащення":
                features = data

            if header == "Призначення":
                scope = data

            if header == "Розмір":
                size = data

            if  header == "Об'єм (л)":
                volume = data

        specs = Specs(
            width=width, length=length, height=height, weight=weight,
            warranty=warranty, wheels=wheels_no, origin=origin, material=material,
            volume_range=volume_range, features=features, scope=scope,
            size=size, volume=volume
        )
        return specs


    def get_luggage_dimension(self, data):
        longest = 0
        medium = 0
        smallest = 0
        m = re.search("([\d.]+)\sx\s([\d.]+)\sx\s([\d.]+)", data)
        if not m:
            return longest, medium, smallest
        vals = [
            float(m.groups()[0]), float(m.groups()[1]), float(m.groups()[2])
        ]
        vals.sort()
        return vals[0], vals[1], vals[2]

