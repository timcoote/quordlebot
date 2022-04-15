# Simple quordle robot

Python(3) based, uses scrapy, although not much, and selenium to run and solve quordle. Set up to drive Chrome. Includes
`requirements.txt` to capture dependency versions.

Initial version has a few bugs in traversing the 4 results boards (the possible combinations use the wrong values for
known locations and non-locations from the wrong boards, much of the time).

If <= 2 possible words are identified, then the first is tried until all 4 words are found or the program fails.

Install with `pip`:
`python3 -m pip install -r requirements.txt`

Modify the location of chromedriver, if necessary (in words/spiders/quordle.py).

Run with `scrapy crawl quordle`. It should spin up an instance of Chrome, try 3 words and try to work out the answers.
The options can be seen in the terminal, if it gets stuck with >2 answers, typing in one into Chrome should get it out
of the loop.
