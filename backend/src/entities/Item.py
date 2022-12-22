class Item:
    def __init__(self, size, brand, image, body_area, weather, is_sport, is_business, category,color):
        self.size = size
        self.brand = brand
        self.image = image
        self.body_area = body_area
        self.weather = weather
        self.is_sport = is_sport
        self.is_business = is_business
        self.category = category
        self.color = color

    def to_dict(self):
        data = {"size": self.size, "brand": self.brand, "image": self.image,
                "bodyArea": self.body_area, "weather": self.weather, "isSport": self.is_sport,
                "isBusiness": self.is_business, "category": self.category, "color": self.color}

        return data

    @staticmethod
    def from_dict(data):
        return Item(data["size"]
                    , data["brand"]
                    , data["image"]
                    , data["bodyArea"]
                    , data["weather"]
                    , data["isSport"]
                    , data["isBusiness"]
                    , data["category"]
                    , data["color"])


