from . import base, reviews, development, training, feedback, contact


def setup_handlers(dp):
    """
    Register all routers in Dispatcher.
    """
    dp.include_router(base.router)
    dp.include_router(reviews.router)
    dp.include_router(development.router)
    dp.include_router(training.router)
    dp.include_router(feedback.router)
    dp.include_router(contact.router)
