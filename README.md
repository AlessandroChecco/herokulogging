# Fast REST logger on Heroku

Append-only, ephemeral in-memory logging REST interface.
https://fast-logging.herokuapp.com/

To keep the app always on, you will need to set the variable CURRENTDOMAIN in heroku app settings, or hardcode it here in clock.py. Remember to enable both dynos (web and clock) in the app overview.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

