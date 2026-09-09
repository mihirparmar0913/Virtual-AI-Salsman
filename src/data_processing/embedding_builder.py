def build_embedding_text(product: dict) -> str:
    """
    Build a concise, structured text representation of a product
    for semantic embedding.
    """

    parts = []

    if product.get("product_name"):
        parts.append(f"Product: {product['product_name']}")

    if product.get("brand"):
        parts.append(f"Brand: {product['brand']}")

    if product.get("main_category"):
        parts.append(f"Category: {product['main_category']}")

    if product.get("product_category"):
        parts.append(f"Product Type: {product['product_category']}")

    if product.get("description"):
        description = str(product["description"]).strip()

        if len(description) > 2000:
            description = description[:2000]

        parts.append(f"Description: {description}")

    features = product.get("features")

    if features:
        feature_text = ", ".join(
            f"{key}: {value}"
            for key, value in features.items()
        )

        parts.append(f"Features: {feature_text}")

    return "\n".join(parts)