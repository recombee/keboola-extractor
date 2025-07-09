import os
import pandas as pd


class InputTable:
    def __init__(self, path: str):
        self.path = path
        self.df = pd.read_csv(self.path)
        self.name = os.path.basename(path).lower()

    def is_items_catalog(self):
        return self.name == "items.csv"

    def is_users_catalog(self):
        return self.name == "users.csv"

    def is_detail_views(self):
        return self.name == "detail_views.csv"

    def is_purchases(self):
        return self.name == "purchases.csv"

    def is_ratings(self):
        return self.name == "ratings.csv"

    def is_bookmarks(self):
        return self.name == "bookmarks.csv"

    def is_cart_additions(self):
        return self.name == "cart_additions.csv"

    def is_view_portions(self):
        return self.name == "view_portions.csv"
