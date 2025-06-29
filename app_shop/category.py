from app_shop.models import Category


def get_subcategories_by_category(category: str) -> list:
    current_category = Category.objects.get(name=category)
    category_set = Category.objects.filter(parent_category_id=current_category.id).all()
    if not len(category_set):
        category_set = [current_category]
    else:
        category_set = list(category_set) + [current_category]
    return category_set
