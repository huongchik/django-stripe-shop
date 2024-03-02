# Project Overview

This project is a Django web application designed to demonstrate e-commerce functionality, including order processing and integration with Stripe for payment processing. The application supports currency conversion and minimum price validation, as well as discounts and taxes when calculating the total cost of an order.

For testing, the application is accessible at http://194.53.54.26:8000/.

## Project Setup

To get the project up and running, follow these steps:

1. Install the project dependencies using `pip install -r requirements.txt`.
2. Set up the database by running Django migrations with `python manage.py migrate`.
3. Create a superuser for access to the Django admin panel using `python manage.py createsuperuser`.
4. Start the development server with `python manage.py runserver`.

Alternatively, you can use Docker to set up and run the project:

1. Build the Docker containers using the command `docker-compose build`.
2. Start the project by running `docker-compose up`.

This will set up the necessary services and start the development server accessible via the configured port.



## Accessing the Admin Panel

By default, accessing the root URL of the project (`http://127.0.0.1:8000/`) redirects to the Django admin panel. Use the following credentials to log in:

- **Username:** huongchi
- **Password:** 2309

## Working with the Application

### Viewing and Creating Products

Navigate to the admin panel to view existing products or add new ones.

### Testing

To test orders, navigate to a URL of the form `http://127.0.0.1:8000/myapp/order/<id>/`, where `<id>` is the order ID. You can also create new orders through the admin panel.

To view or test individual items, navigate to a URL of the form `http://127.0.0.1:8000/myapp/item/<id>/`, where `<id>` is the item ID. This allows you to see the item details page. New items can be added or existing items can be edited through the admin panel.



## Stripe Configuration

To work with Stripe's payment system, you have two options for configuring the API keys in your project. You can either directly set them in your project's `myproject/settings.py` file or use a `myproject/.env` file (which is the recommended approach for better security and flexibility).

### Direct Configuration in `settings.py`

You can directly set the API keys in your `settings.py` file as follows:

```python
STRIPE_PUBLIC_KEY = 'your_public_key'
STRIPE_SECRET_KEY = 'your_secret_key'
```

### Using a .env File (Recommended)
```python
STRIPE_PUBLIC_KEY=your_public_key
STRIPE_SECRET_KEY=your_secret_key
```

