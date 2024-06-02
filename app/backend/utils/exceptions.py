from fastapi import status

class NoCategoryError(Exception):
    descr = status.HTTP_404_NOT_FOUND
    detail = "Category not found!"


class NoProductByCategoryError(Exception):
    descr = status.HTTP_404_NOT_FOUND
    detail = "Products by that category slug not found!"
