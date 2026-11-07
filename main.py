from aims.dvd import DigitalVideoDisc
from aims.cart import Cart


def main():
    cart = Cart()
    cart.add_dvd(DigitalVideoDisc("The Lion King", "Animation", "Roger Allers", 87, 19.95))
    cart.add_dvd(DigitalVideoDisc("Star Wars", "Science Fiction", "George Lucas", 87, 24.95))
    cart.add_dvd(DigitalVideoDisc("Aladdin", "Animation", cost=18.99))
    print(f"Total cost: {cart.total_cost():.2f} $")


if __name__ == "__main__":
    main()
