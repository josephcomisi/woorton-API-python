from APIWoorton import APIWoorton


def main():
    """
    Example of Woorton API use
    You need a token provided by Woorton team to use the API
    """

    # Create object
    woorton = APIWoorton(token='TOKENHERE')

    # Help on functions
    woorton.help()

    """ Account details """

    # List of instruments
    # print woorton.instruments()

    # List of balances
    # print woorton.balances()

    # List of trades
    # print woorton.trades()

    # List of operations
    # print woorton.ledger()

    # List of exposures (available soon)
    # print woorton.exposures()

    """ Trading """

    # Request For Quote
    # print woorton.request_for_quote(amount=1.0, instrument='BTCEUR.SPOT', direction='buy')

    # Execute RFQ
    # print woorton.execute()

    # State of execution
    # print woorton.state


if __name__ == '__main__':
        main()