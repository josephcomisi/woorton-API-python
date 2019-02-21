from APIWoorton import APIWoorton


def main():
    """
    Example of Woorton API use
    You need a token provided by Woorton team to use the API
    """

    # Create object
    woorton = APIWoorton(token='TOKEN_HERE')

    # Help on functions
    woorton.help()

    """ Account details """

    # List of instruments
    # print woorton.instrument_list

    # List of balances
    # print woorton.balances()

    # List of trades
    # print woorton.trades()

    # List of operations
    # print woorton.ledger()

    # List of exposures
    # print woorton.exposures()
    
    # List of remaining exposures
    # print woorton.remaining_exposures()

    """ Trading """

    # 1) Request For Quote
    # print woorton.request_for_quote(amount=1.0, instrument='BTCEUR.SPOT', direction='buy')

    # 2) Execute RFQ
    # print woorton.execute()

    # 3) State of execution
    # print woorton.state
    
    # Or alternatively:
    # print woorton.market_order(amount=1.0, instrument='BTCEUR.SPOT', direction='buy')
    

if __name__ == '__main__':
        main()