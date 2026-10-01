import products
import promotions
from store import Store


def get_integer(message):
    """Ask the user for an integer and keep retrying until valid."""
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Please enter a valid number.")


def get_choice(message, minimum, maximum):
    """Ask for an integer within a specified range."""
    while True:
        choice = get_integer(message)

        if minimum <= choice <= maximum:
            return choice

        print(f"Please enter a number between {minimum} and {maximum}.")


def get_yes_no(message):
    """Ask the user for a yes/no answer."""
    while True:
        answer = input(message).strip().lower()

        if answer in ("y", "n"):
            return answer

        print("Please enter y or n.")


def get_available_quantity(product, shopping_list):
    """Return the quantity available after accounting for the cart."""
    ordered_quantity = sum(
        quantity
        for ordered_product, quantity in shopping_list
        if ordered_product == product
    )

    return product.get_quantity() - ordered_quantity


def show_menu():
    """Display the store's main menu."""
    print(
        "1. List all products in store\n"
        "2. Show total amount in store\n"
        "3. Make an order\n"
        "4. Quit\n"
    )


def list_products(store):
    """Display all active products in the store."""
    available_products = store.get_all_products()

    if not available_products:
        print("There are no products currently available.\nThe store is sold out.")
        return

    for index, product in enumerate(available_products, start=1):
        print(f"{index}. ", end="")
        product.show()

    print()


def show_total_quantity(store):
    """Display the total quantity of products in the store."""
    print(f"Total amount of products: {store.get_total_quantity()}\n")


def get_orderable_products(store, shopping_list):
    """Return products still available for the current order."""
    return [
        product for product in store.get_all_products()
        if not product.is_stocked()
           or get_available_quantity(product, shopping_list) > 0
    ]


def add_product_to_order(available_products, shopping_list):
    """Ask the user to select a product and quantity."""
    print("\nAvailable products:")

    for index, product in enumerate(available_products, start=1):
        available_quantity = get_available_quantity(
            product,
            shopping_list
        )

        if product.is_stocked():
            quantity_text = f"Quantity: {available_quantity}"
        else:
            quantity_text = "Non-stocked"

        promotion_text = (
            f", Promotion: {product.promotion.name}"
            if product.promotion
            else ""
        )

        maximum_text = (
            f", Maximum: {product.maximum}"
            if isinstance(product, products.LimitedProduct)
            else ""
        )

        print(
            f"{index}. "
            f"{product.name}, "
            f"Price: {product.price}, "
            f"{quantity_text}"
            f"{maximum_text}"
            f"{promotion_text}"
        )

    product_choice = get_choice(
        "Please enter the product number: ",
        1,
        len(available_products)
    )

    product = available_products[product_choice - 1]

    available_quantity = get_available_quantity(
        product,
        shopping_list
    )

    if product.is_stocked():
        maximum_quantity = available_quantity

        if isinstance(product, products.LimitedProduct):
            maximum_quantity = min(
                available_quantity,
                product.maximum
            )

        quantity = get_choice(
            "\nPlease enter the quantity: ",
            1,
            maximum_quantity
        )
    else:
        quantity = get_integer(
            "\nPlease enter the quantity: "
        )

        while quantity <= 0:
            print("Please enter a positive quantity.")
            quantity = get_integer(
                "\nPlease enter the quantity: "
            )

    shopping_list.append((product, quantity))

    print(
        f"\n{quantity} {product.name} "
        "added to the shopping list.\n"
    )


def make_order(store):
    """Collect products and quantities and process an order."""
    shopping_list = []

    while True:
        available_products = get_orderable_products(store, shopping_list)

        if not available_products:
            print("There are no more products available to add.")
            break

        add_product_to_order(available_products, shopping_list)

        another = get_yes_no("Would you like to add another product? (y/n): ")

        if another == "n":
            break

    if shopping_list:
        try:
            total = store.order(shopping_list)
            print(f"\nTotal price: ${total}\n")
        except ValueError as error:
            print(f"Order could not be completed: {error}")


def start(store):
    """Run the store's main menu."""
    actions = {
        1: lambda: list_products(store),
        2: lambda: show_total_quantity(store),
        3: lambda: make_order(store),
    }

    while True:
        show_menu()

        choice = get_choice("Please choose an option: ", 1, 4)

        if choice == 4:
            print("Goodbye!")
            break

        actions[choice]()


def main():
    """Create the store and start the application."""
    # Setup initial stock of inventory
    product_list = [
        products.Product("MacBook Air M2", price=1450, quantity=100),
        products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        products.Product("Google Pixel 7", price=500, quantity=250),
        products.NonStockedProduct("Windows License", price=125),
        products.LimitedProduct("Shipping", price=10, quantity=250, maximum=1),
    ]

    # Create promotion catalog
    second_half_price = promotions.SecondHalfPrice("Second Half price!")
    third_one_free = promotions.ThirdOneFree("Third One Free!")
    thirty_percent = promotions.PercentDiscount("30% off!", percent=30)

    # Add promotions to products
    product_list[0].set_promotion(second_half_price)
    product_list[1].set_promotion(third_one_free)
    product_list[3].set_promotion(thirty_percent)

    best_buy = Store(product_list)

    start(best_buy)


if __name__ == "__main__":
    main()
