from google.appengine.ext import webappfrom google.appengine.ext import dbfrom google.appengine.api import usersfrom helperfunctions import *# Handler posted to by the add frame on the add capital frameclass AddCapital(webapp.RequestHandler):    def post(self):        current_user = UserCapital.gql("WHERE name = :1", users.get_current_user()).fetch(1)        try:            exact_amount = math.fabs(float(self.request.get('amount')))            amount = round(exact_amount, 2)        except ValueError:            # Bad input value            ERROR = ErrorMessage()            ERROR.error_string = self.request.get('amount') + " is not a valid amount."            ERROR.put()            self.redirect('/logged_in/frames/frame_add_capital.html')            return        # If user has a capital value, add to it. If not, create one.        if current_user:            entry = current_user.pop(0)            entry.free_capital += amount            entry.put()        else:            current_user = UserCapital()            current_user.name = users.get_current_user()            current_user.free_capital = amount            current_user.put()                CONFIRM = ConfirmMessage()        CONFIRM.confirm_string = "Successfully added $" + str(amount)        CONFIRM.put()                # Add history entry        current_history = UserHistory.gql("WHERE name = :1", users.get_current_user()).fetch(1)        if current_history:            hist = current_history.pop(0)        else:            hist = UserHistory()            hist.name = users.get_current_user()        hist.types.append("capital")        hist.dates.append(datetime.datetime.now())        hist.symbols.append("")        hist.prices.append(amount)        hist.shares.append(0)        hist.buy.append(True)        hist.put()        self.redirect('/logged_in/frames/frame_add_capital.html')        # Handler posted to by the remove form on the add capital frameclass RemoveCapital(webapp.RequestHandler):    def post(self):        current_user = UserCapital.gql("WHERE name = :1", users.get_current_user()).fetch(1)        try:            exact_amount = math.fabs(float(self.request.get('amount')))            amount = round(exact_amount, 2)        except ValueError:            # Bad input value            ERROR = ErrorMessage()            ERROR.error_string = self.request.get('amount') + " is not a valid amount."            ERROR.put()            self.redirect('/logged_in/frames/frame_add_capital.html')            return        # If user has enough capital, remove 'amount' from it.        if current_user and current_user[0].free_capital >= amount:            entry = current_user.pop(0)            entry.free_capital -= amount            entry.put()        else:            # User does not have enough money.            ERROR = ErrorMessage()            ERROR.error_string = "You do not have enough money."            ERROR.put()            self.redirect('/logged_in/frames/frame_add_capital.html')            return                CONFIRM = ConfirmMessage()        CONFIRM.confirm_string = "Successfully removed $" + str(amount)        CONFIRM.put()                # Add history entry        current_history = UserHistory.gql("WHERE name = :1", users.get_current_user()).fetch(1)        if current_history:            hist = current_history.pop(0)        else:            hist = UserHistory()            hist.name = users.get_current_user()        hist.types.append("capital")        hist.dates.append(datetime.datetime.now())        hist.symbols.append("")        hist.prices.append(-amount)        hist.shares.append(0)        hist.buy.append(True)        hist.put()        self.redirect('/logged_in/frames/frame_add_capital.html')# Buy and Sell Class. This class gets the quoted stock price and the amount of shares needed to be purchased. # After calculating the total and going through the error checking, it stores the values in the UserHistory Database.# It then goes through to see if the stock is already in the UserStock Database and edits the rest of it. If it doesn't# exist in the Database, it creates an entry for it first. class BuySell(webapp.RequestHandler):    def post(self):        symbol = self.request.get('symbol')        symbol = symbol.upper()        shares = self.request.get('shares')        buysell = self.request.get('buysell')        get_quote = quote(symbol)        current_price = float(get_quote[1])        try:            total = current_price * float(shares)        except ValueError:            ERROR = ErrorMessage()            ERROR.error_string = "Please enter a valid quantity."            ERROR.put()            self.redirect('/logged_in/frames/frame_buy_sell.html')            return                if stock_is_valid(symbol) and int(shares) > 0:            if buysell == "Buy":                current_user = UserCapital.gql("WHERE name = :1", users.get_current_user()).fetch(1)                if current_user:                    entry = current_user.pop(0)                    if entry.free_capital > float(total):                        entry.free_capital -= float(total)                        entry.put()                                        # Add to history database (don't condense stocks together, just raw data)                        history_stock = UserHistory.gql("WHERE name = :1", users.get_current_user()).fetch(1)                         if history_stock: # Does the user already have a user history?                            history_stock2 = history_stock.pop(0)                        else: # If not, create one.                            history_stock2 = UserHistory()                            history_stock2.name = (users.get_current_user())                                            history_stock2.types.append("buy")                        history_stock2.symbols.append(symbol)                        history_stock2.prices.append(float(current_price))                        history_stock2.shares.append(int(shares))                        history_stock2.buy.append(True)                        history_stock2.dates.append(datetime.datetime.now())                        history_stock2.put()                                                          current_stock = UserStocks.gql("WHERE name = :1", users.get_current_user()).fetch(1)                                         if current_stock: # Do they own any stocks already?                            current_stock2 = current_stock.pop(0)                            if symbol in current_stock2.stocks: # If they already have that stock purchased, don't append anything.                                i = current_stock2.stocks.index(symbol)                                current_stock2.amt_spent[i] += float(total)                                current_stock2.shares[i] += int(shares)                            else: # Append new information to the user's list of stocks.                                 current_stock2.amt_spent.append(float(total))                                current_stock2.shares.append(int(shares))                                current_stock2.stocks.append(symbol)                                                                        else: # Create a stocks database.                            current_stock2 = UserStocks()                            current_stock2.name = users.get_current_user()                            current_stock2.stocks.append(symbol)                            current_stock2.shares.append(int(shares))                            current_stock2.amt_spent.append(float(total))                                                current_stock2.put()                CONFIRM = ConfirmMessage()                CONFIRM.confirm_string = "Stock successfully bought!!"                CONFIRM.put()                self.redirect('/logged_in/frames/frame_buy_sell.html')            else:                current_stock = UserStocks.gql("WHERE name = :1", users.get_current_user()).fetch(1)                current_user = UserCapital.gql("WHERE name = :1", users.get_current_user()).fetch(1)                if current_stock:                    entry = current_stock.pop(0)                    entry2 = current_user.pop(0)                    if symbol in entry.stocks:                        i = entry.stocks.index(symbol)                        if entry.shares[i] >= int(shares):                            entry.shares[i]-=int(shares)                            entry.amt_spent[i]-=float(total)                            entry2.free_capital += float(total)                            entry.put()                            entry2.put()                                                    history_stock = UserHistory.gql("WHERE name = :1", users.get_current_user()).fetch(1)                             if history_stock: # Does the user already have a user history?                                history_stock2 = history_stock.pop(0)                            else: # If not, create one.                                history_stock2 = UserHistory()                                history_stock2.name = (users.get_current_user())                                                        history_stock2.types.append("sell")                            history_stock2.symbols.append(symbol)                            history_stock2.prices.append(float(current_price))                            history_stock2.shares.append(int(shares))                            history_stock2.buy.append(False)                            history_stock2.dates.append(datetime.datetime.now())                            history_stock2.put()                CONFIRM = ConfirmMessage()                CONFIRM.confirm_string = "Stock successfully sold!!"                CONFIRM.put()        elif not stock_is_valid(symbol):            ERROR = ErrorMessage()            ERROR.error_string = self.request.get('symbol') + " is not a valid stock."            ERROR.put()        else:            ERROR = ErrorMessage()            ERROR.error_string = "Please enter a quantity greater than zero."            ERROR.put()        self.redirect('/logged_in/frames/frame_buy_sell.html')        class AddWatch(webapp.RequestHandler):    def post(self):        uw = UserWatches()        # Set the user to the current user        if users.get_current_user():            uw.name = users.get_current_user()        # Retrieve the value of watchlist from the form        temp_stock = self.request.get('watchlist')        temp_stock = temp_stock.upper()        # Create a copy of the content of UserWatches        temp_db = UserWatches.all()        # Filter out all items belonging to anyone besdies the current user        temp_db.filter("name =",users.get_current_user())                # Prevent the input of a non-real stock        stockquote = quote(temp_stock)        if stockquote[6] != "N/A":             temp_list = temp_db.fetch(100)                        test_bool = "true"            # Cycle through the list.  If any of the current stocks are            # equal to the entered stock, set the flag to false            for i in range(0,len(temp_list)):                if temp_stock == temp_list[i].stocks:                    test_bool = "false"            # Unless the flag goes false, enter the stock into the database            if test_bool == "true":                uw.stocks = temp_stock                 uw.put()        else:            ERROR = ErrorMessage()            ERROR.error_string = self.request.get('watchlist') + " is not a valid stock."            ERROR.put()        self.redirect('/logged_in/frames/frame_watch_list.html')        class DeleteWatch(webapp.RequestHandler):    def post(self):        watchlist = UserWatches()                # Get the name of the stock to be deleted        deletion_candidate = self.request.get('deletion_candidate')        deletion_candidate = deletion_candidate.upper()        current_user = users.get_current_user()        # Get a list of all stocks belonging to the current user, with the entered name        q = db.GqlQuery("SELECT __key__ FROM UserWatches WHERE name = :1 AND stocks = :2", current_user, deletion_candidate)        # Due to the copy-checking of the add function,        # we know there can be only one entry that meets our criteria        results = q.fetch(1)        # Delete the list 'results' from the database        db.delete(results)        if len(results) == 0:            ERROR = ErrorMessage()            ERROR.error_string = self.request.get('deletion_candidate') + " is not being currently watched."            ERROR.put()        self.redirect('/logged_in/frames/frame_watch_list.html')                #the handler for the settings form found in logged_in/settings.htmlclass GetSettings(webapp.RequestHandler):    def post(self):        settings = UserSettings()                if users.get_current_user():            settings.author = users.get_current_user()                settings.defaultcurrency = self.request.get('currency')        settings.put()        self.redirect('/logged_in/settings.html')#puts the new setting into the settings datastore and redirects back to /logged_in/settings.html