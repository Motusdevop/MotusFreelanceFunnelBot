from models import Review


def format_review(review: Review) -> str:
    """
    Format review entity into human-readable text for Telegram.
    """
    date_str = (
        review.date.strftime("%d.%m.%Y %H:%M")
        if hasattr(review.date, "strftime")
        else str(review.date)
    )
    return (
        f"<b>{review.name}</b> — {review.service}\n"
        f"Оценка: {review.grade}/5 {''.join(['⭐' for _ in range(review.grade)])}\n"
        f"<i>{date_str}</i>\n\n"
        f"{review.review}\n\n"
        f"{review.additionally or ''}"
    )


def format_user_activity(client) -> str:
    """
    Format user activity information for admin notifications.
    """
    return (
        "User activity:\n\n"
        f"first_name: {client.first_name}\n"
        f"last_name: {client.last_name}\n"
        f"chat_id: {client.chat_id}\n"
        f"username: {client.username}\n\n"
        f"clicked button: {client.callback_data}"
    )
