def categorize(article):
    text = (article["title"] + " " + article["summary"]).lower()

    if "rate" in text:
        return "Interest Rates"
    if "cfpb" in text or "regulation" in text:
        return "Regulation"
    if "ai" in text or "technology" in text:
        return "Technology"

    return "General"


def tag(article):
    tags = []

    if "refinance" in article.get("summary", "").lower():
        tags.append("Refi Opportunity")

    if "purchase" in article.get("summary", "").lower():
        tags.append("Purchase Market")

    return tags
