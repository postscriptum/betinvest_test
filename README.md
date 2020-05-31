## Sport Results Parser

*client.py* module scrapes sport results from the site https://www.fonbet.ru/results/
The results are stored in Redis.

*server.py* module displays the results as table.
- http://127.0.0.1:8080/ - returns all results
- http://127.0.0.1:8080/{begin_string} - returns results with names begining with specified string
