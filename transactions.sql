CREATE TABLE transactions (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, user_id INTEGER NOT NULL, symbol TEXT NOT NULL, shares INTEGER NOT NULL, price_per_share NUMERIC NOT NULL, time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)