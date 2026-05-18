# Create your models here.
from bson import ObjectId

class Person:
    def __init__(self, name, document, email, phone, invoices=None):
        self.name = name
        self.document = document
        self.email = email
        self.phone = phone
        self.invoices = invoices if invoices is not None else []

    def is_valid(self):
        errors = []

        if not (3 <= len(self.name) <= 100):
            errors.append("Name must be between 3 and 100 characters.")

        if not (4 <= len(self.document) <= 20):
            errors.append("Document must be between 4 and 20 characters.")

        if not (6 <= len(self.email) <= 100):
            errors.append("Email must be between 6 and 100 characters.")

        if not (6 <= len(self.phone) <= 15):
            errors.append("Phone must be between 6 and 15 characters.")

        if not isinstance(self.invoices, list):
            errors.append("Invoices must be a list.")
        else:
            for invoice in self.invoices:
                if not isinstance(invoice, ObjectId):
                    errors.append("Each invoice must be a valid ObjectId.")

        return errors

    def to_dict(self):
        return {
            "name": self.name,
            "document": self.document,
            "email": self.email,
            "phone": self.phone,
            "invoices": self.invoices
        }