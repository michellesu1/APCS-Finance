import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set


@app.after_request
def after_request(response):
  """Ensure responses aren't cached"""
  response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
  response.headers["Expires"] = 0
  response.headers["Pragma"] = "no-cache"
  return response


@app.route("/")
@login_required
def index():
  """Show portfolio of stocks"""
  stock_shares = {};
  transactions = db.execute("SELECT * FROM transactions WHERE user_id = ?", session['user_id']); #list of dicts
  for transaction in transactions:
    symbol = transaction['symbol'];
    shares = transaction['shares'];
    if symbol not in stock_shares:
      stock_shares[symbol] = shares;
    else:
      stock_shares[symbol] += shares;

  stocks=[]
  for symbol in stock_shares:
    price = lookup(symbol)['price'];
    shares = stock_shares[symbol];
    value = price*shares;
    stock = {'symbol': symbol, 'shares': shares, 'price': price, 'value': value};
    stocks.append(stock);

  
  
  
  return apology("TODO")
  

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
  """Buy shares of stock"""
  if request.method == "GET":
    return render_template("buy.html");
  else:
    shares = request.form.get("shares");
    if not shares or not(shares.isdigit() and int(shares)>0):
      return apology("input positive integer for number of shares")
    shares = int(shares);
    symbol = request.form.get("symbol");
    price = lookup(symbol)['price'];
    user_id = session["user_id"];

    total_price = price*shares;
    user_cash = db.execute("SELECT * FROM users WHERE id = ?", user_id)[0]["cash"];

    if (user_cash<total_price):
      return apology("you are too poor");
    db.execute("INSERT INTO transactions (user_id, symbol, shares, price_per_share) VALUES (?, ?, ?, ?)", user_id, symbol, shares, price);
    user_cash-=total_price;
    db.execute("UPDATE users SET cash=? WHERE id = ?", user_cash, user_id)
    return redirect("/buy")
    
      



@app.route("/history")
@login_required
def history():
  """Show history of transactions"""
  return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
  """Log user in"""

  # Forget any user_id
  session.clear()

  # User reached route via POST (as by submitting a form via POST)
  if request.method == "POST":

    # Ensure username was submitted
    if not request.form.get("username"):
      return apology("must provide username", 403)

    # Ensure password was submitted
    elif not request.form.get("password"):
      return apology("must provide password", 403)

    # Query database for username
    rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

    # Ensure username exists and password is correct
    if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
      return apology("invalid username and/or password", 403)

    # Remember which user has logged in
    session["user_id"] = rows[0]["id"]

    # Redirect user to home page
    return redirect("/")

  # User reached route via GET (as by clicking a link or via redirect)
  else:
    return render_template("login.html")


@app.route("/logout")
def logout():
  """Log user out"""

  # Forget any user_id
  session.clear()

  # Redirect user to login form
  return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
  """Get stock quote."""

  if request.method == "GET":
    return render_template("quote.html")
  else:
    symbol = request.form.get("symbol");
    price = lookup(symbol)['price'];
    return render_template("quoted.html", symbol = symbol, price = price);
    
  return apology("TODO")


@app.route("/register", methods=["GET", "POST"])
def register():
  """Register user"""
  #password and confirmation equal, username not taken
  if request.method == "GET":
    return render_template("register.html")
  else:
    username = request.form.get("username");
    if not username:
      return apology("must provide username", 403)
    rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
    if len(rows)!=0:
      return apology("username already taken", 403)


    password = request.form.get("password");
    confirmation = request.form.get("confirmation");
    if not password or not confirmation:
      return apology("must provide password and password confirmation")
    elif password!=confirmation:
      return apology("password must be the same as password confirmation", 403)

    hash = generate_password_hash(password);
    session["user_id"] = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
    return redirect("/")
  
    


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
  """Sell shares of stock"""
  return apology("TODO")


app.run(host='0.0.0.0', port=81)
