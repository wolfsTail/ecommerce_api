from fastapi import status


class YouAreNotAdmin(Exception):
    descr = status.HTTP_401_UNAUTHORIZED
    detail = "You are not an admin!"    


class IncorrectCredentailsError(Exception):
    descr=status.HTTP_401_UNAUTHORIZED,
    detail = 'Invalid credentails'


class NoItemError(Exception):
    descr = status.HTTP_404_NOT_FOUND
    detail = "Item is not found"


class NoUserError(NoItemError):
    descr = status.HTTP_404_NOT_FOUND
    detail = "User is not found"


class NotTheOwnerOfProduct(Exception):
    descr = status.HTTP_403_FORBIDDEN
    detail = "You are not a owner of this product!"      


class NoUserCredentials(Exception):
    descr = status.HTTP_403_FORBIDDEN
    detail = "You have no need credentials to do this method!"  


class NoProductBySlugError(Exception):
    descr = status.HTTP_404_NOT_FOUND
    detail = "Product not found!"


class NoCategoryError(Exception):
    descr = status.HTTP_404_NOT_FOUND
    detail = "Category not found!"


class NoProductByCategoryError(Exception):
    descr = status.HTTP_404_NOT_FOUND
    detail = "Products by that category slug not found!"
