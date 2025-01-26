# Ecommerce-API

The Ecommerce API project is build to test my skill on Django RESTFramework(DRF). It includes functionalities such as user authentication, product management, category management, order processing, and cart handling.This is the basic version of the API.The updated version with additional features such payment will be done later.

---

## **Contact ME**
>If you have any query or remarks or you find bug related to this fell free to contact  me.
>Email: [akash2005k26kaniyur12@gmail.com](mailto:akash2005k26kaniyur12@gmail.com)

---

## **Features:**
1. User authentication (Register, Login, Logout)
2. Product management (List, Create, Update, Delete)
3. Category management
4. Shopping cart functionality
5. Order management
6. Search functionality for products and categories

---

## **Requirments:**
Make sure you have the following installed before running the project:
- Python 
- Django
- Django RestFramework
- pillow

---

## **NOTE:**
>The debug is set `False` (debug=False) in the settings so make sure you turn it `True` if you are running this project locally.
>Ensure to configure the `ALLOWED_HOSTS` setting appropriately for your environment.  
>There is no model data with this project

---

## **Views**
Here are the details about the viwes in API

### 1. Authentication Views
  1. RegisterView:
      - Handles user registration.
      - Uses ProfileSerializer for creating ProfileModel instances.
  2. LoginView:
      - Authenticates a user using username and password.
      - Returns an authentication token if login is successful.
  3. LogoutView:
      - Deletes the user's authentication token, effectively logging them out.
### 2. Product Views
  1. ProductListCreateView:
      - Lists all products with non-zero inventory.
      - Allows staff users to create new products.
  2. ProductDetailView:
      - Retrieves details of a specific product by its primary key (pk).
      - Returns a custom response if the product is out of stock.
  3. ProductUpdateView:
      - Updates product details.
      - Ensures the product description is set to the name if not provided.
  4. ProductDeleteView:
      - Deletes a product by its primary key (pk).
      - Returns the deleted product's data as a confirmation.
### 3. Category Views
  1. CategoryListCreatView:
      - Lists all categories.
      - Allows staff users to create new categories.
  2. CategoryDetailView:
      - Retrieves details of a specific category and its products.
  3. CategoryDeleteView:
      - Deletes a category by its primary key (pk).
### 4. Search View
  1. searchView:
      - Searches for products and categories based on a query parameter (key).
      - Returns both products and categories that match the search term.
### 5. Order Views
  1. ListCreateOrderView:
      - Lists all orders of a user categorized as "Pending," "Shipped," or "Other."
      - Creates a new order if sufficient product inventory is available.
  2. OrderDetailView:
      - Retrieves details of a specific order item by its primary key (pk).
  3. OrderStatusUpdateView:
      - Updates the status of an order.
      - Requires the primary key of the order to update.
### 6. Cart Views
  1. CartAddListView:
      - Lists all items in a user's cart.
      - Allows users to add items to their cart.
  2. CartDetailView:
      - Retrieves details of a specific cart item, including the total price.
  3. CartRemoveView:
      - Deletes a specific cart item.
### 7. Fallback View
  1. PageNotFoundView:
      - Returns a custom 404 response for non-existent URLs.

---

>Thank you for spending your valuable time on exploring my project.
>If you have any remarks please fell free to contact me!
