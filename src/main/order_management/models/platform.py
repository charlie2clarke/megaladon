'''Represents data stored online retailer order was from.

Currently is setting default values. Is in place for future
intended development to allow cross-platform functionality.
'''


class Platform:
    '''Represents data for access online store via API.

    Attributes:
        platform: a string of online retailer.
        user_token: a string of API bearer token needed to
                    access online store via API.
    '''
    platform = "ebay"
    user_token = "abc123"
