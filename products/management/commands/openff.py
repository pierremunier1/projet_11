
#from products.model.articles import Product

from . import config
import requests
from products.models import Product,Category
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError, DataError
from django.core.exceptions import ValidationError
from django.db import transaction, IntegrityError

class Command(BaseCommand):

    """Requests data to the OpenFoodFacts API to fill the local database
    with data (food, food categories)"""

    print('working')

    help = "populate the database via OpenFoodFacts API"

    def handle(self, *args, **options):
        """asq openfoodfact api and retrieve datas"""

        self.categories = config.CATEGORIES
    
        """get all products from openfoodfact api."""
        for category in self.categories:

            params = {
                "action": "process",
                "tagtype_0": "categories",
                "tag_contains_0": "contains",
                "tag_0": category,
                "tagtype_1": "countries",
                "tag_contains_1": "contains",
                "tag_1": "france",
                "page": 1,
                "page_size": config.PAGE_SIZE,
                "json": 1,
            }

            res = requests.get(
                "https://fr.openfoodfacts.org/cgi/search.pl", params=params
            )

            self.result = res.json()
            self.products = self.result["products"]

            for product in self.products:

                # check if all field are presents

                self.products = [
                    product.update(categories=category)
                    for product in self.result["products"]
                ]

                if not all(tag in product for tag in config.FILTER):
                    continue
                elif len(product["quantity"]) == 0:
                    continue
                elif len(product["nutrition_grade_fr"]) == 0:
                    continue
                elif len(product["image_nutrition_url"]) == 0:
                    continue
                
                code = product["code"]
                product_name = product["product_name"]
                category_name = product["categories"]
                nutriscore = product["nutrition_grade_fr"]
                nutriscore_100g = product['nutriments']["nutrition-score-fr_100g"]
                brands = product["brands"]
                url = product["url"]
                image_food = product["image_front_thumb_url"]
                image_nutrition = product["image_nutrition_url"]
                
                 # Prints for the Console Command Line

                self.stdout.write("Nom : {}".format(product_name))
                self.stdout.write("Marque : {}".format(brands))
                self.stdout.write("Image de l'aliment : {}".format(image_food))
                self.stdout.write("Image repères nutritionnels : {}".format(image_nutrition))
                self.stdout.write("Nutriscore : {}".format(nutriscore))
                self.stdout.write("Nutriscore_100g : {}".format(nutriscore_100g))
                self.stdout.write("URL fiche aliment : {}".format(url))
                self.stdout.write("Catégorie : {}".format(category_name))
                self.stdout.write("N° de l'aliment : {}\n\n".format(code))
                

                try:
                    print("insert")
                    # products are injected in database
                    with transaction.atomic():

                        c1, created = Category.objects.get_or_create(
                            category_name=category_name
                            )

                        p1=Product.objects.create(
                            id=code,
                            product_name=product_name,
                            nutriscore_fr=nutriscore,
                            nutriscore_100g=nutriscore_100g,
                            category=c1,
                            product_url=url,
                            brands=brands,
                            image_food=image_food,
                            image_nutrition=image_nutrition
                            )
                        
                    
                except IntegrityError:
                    self.stdout.write(self.style.WARNING(
                        "Problème : {} n'a pas pu être enregistré dans la base de données.".format(product_name)))

                