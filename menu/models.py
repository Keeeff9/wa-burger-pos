CATEGORIES = ["MAIN", "APETIZER", "DESSERT", "DRINK"]

class Product:
    def __init__(self, name, price, category, has_stock, description=""):
        self.name = name
        self.price = price
        self.category = category
        self.has_stock = has_stock
        self.description = description

    def is_valid(self):
        errors = []

        if not (3 <= len(self.name) <= 50):
            errors.append("Name must be between 3 and 50 characters.")

        if not (500 <= self.price <= 10000000):
            errors.append("Price must be between 500 and 10,000,000.")

        if self.category not in CATEGORIES:
            errors.append(f"Category must be one of: {CATEGORIES}")

        if not isinstance(self.has_stock, bool):
            errors.append("has_stock must be True or False.")

        if self.description and not (3 <= len(self.description) <= 500):
            errors.append("Description must be between 3 and 500 characters.")

        return errors

    def to_dict(self):
        return {
            "name": self.name,
            "price": self.price,
            "category": self.category,
            "has_stock": self.has_stock,
            "description": self.description,
        }