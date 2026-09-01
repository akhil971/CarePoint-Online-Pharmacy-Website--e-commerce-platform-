def cart_wishlist_counts(request):
    """
    Makes wishlist_count and cart_count available in every template
    (used for the heart / cart badge numbers in the navbar).
    """
    wishlist_count = 0
    cart_count = 0

    if request.user.is_authenticated:
        wishlist_count = request.user.wishlist_items.count()
        cart_count = sum(
            item.quantity for item in request.user.cart_items.all()
        )

    return {
        'wishlist_count': wishlist_count,
        'cart_count': cart_count,
    }
