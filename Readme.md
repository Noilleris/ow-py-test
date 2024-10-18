from pyexpat.errors import messagesfrom pyexpat.errors import messages

# General approach
Let's start with the project structure. At first glance, we could split it into two parts, a backend and a frontend. Nice and simple :).

Can we split it any further? Let's pay attention to the backend part.

## Backend
At first glance, it is a simple Python parser/tokenizer, retrieving aggregated information about API usage.

```json
{
    "usage": [
      {
        "message_id": "number",
        "timestamp": "string",
        "report_name": "string?",
        "credits_used": "number"
      }
    ]
}
```

From the data structure, we could already deduce our first step and define classes to represent the data we are working with.

```python
class UsageEntry:
    message: str
    timestamp: str
    report_name: Optional[str]
    credits_used: float

    def __init__(self, message: str, timestamp: str, credits_used: float, report_name: Optional[str] = None):
        self.message = message
        self.timestamp = timestamp
        self.report_name = report_name
        self.credits_used = credits_used
```

The class will allow us to represent a usage entry, and process its fields if needed.

```python
class Usage:
    usage: list<UsageEntry>{}

    def __init__(self):
        self.usage = list<UsageEntry>{}

    def parse_json(self, string):
        # ...

    def serialise(self):
        # ...
```

The second class will cover the structure of the JSON and will serve as an entry point for our data. For the sake of simplicity and keeping in mind that JSON operations have been implemented many times and are straightforward, I'll omit the implementation of parse and serialise functions.

Let's see what we could do with our data. After we passed the appropriate json we need to check for the credits used. There are two cases here.
The first would be to ask an external API if we have a usage, in case of 404 for particular report or if the report id is missing we need to calculate it manually.

We have defined our data. What's next? The API endpoint and the credit usage calculations.

# Calculations

The rules are:

> The number of credits consumed by each message is calculated as follows:
> (**Note:** A “word” is defined as any continual sequence of letters, plus ‘ and -)
> - **Base Cost:** Every message has a base cost of 1 credit.
> - **Character Count:** Add 0.05 credits for each character in the message.
> - **Word Length Multipliers:**
>   - For words of 1-3 characters: Add 0.1 credits per word.
>   - For words of 4-7 characters: Add 0.2 credits per word.
>   - For words of 8+ characters: Add 0.3 credits per word.
> - **Third Vowels:** If any third (i.e. 3rd, 6th, 9th) character is an uppercase or lowercase vowel (a, e, i, o, u) add 0.3 credits for each occurrence.
> - **Length Penalty:** If the message length exceeds 100 characters, add a penalty of 5 credits.
> - **Unique Word Bonus: If all words in the message are unique (case-sensitive), subtract 2 credits from the total cost (remember the minimum cost should still be 1 credit).**
> - **Palindromes:** If the entire message is a palindrome (that is to say, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward), double the total cost after all other rules have been applied.

Let's take a look how we could do the calculations.
```python 
    # ...
    total_cost = 1 # because of the base cost
    total_cost += len(message)*0.05 # for the character count
    total_cost += 100 if len(message) >= 100 # length penalty
```

We have covered the simple cases. Now to the more complex:
```python 
    # ...
    def get_every_third_vowel(input_string):
        return re.findall(r'[aeiouAEIOU]', input_string[::3]).count
    
    total_cost += get_every_third_vowel()*0.35 # for the vowel count
```
This will allow us to pull every third vowel and count it towards credits.

*Note*: Every third is not clear, do we include elem 0?

Now we need to cleanup the string to prepare it for further calculations:

```python 
    # ...
    def extract_words(input_string):
        words = re.findall(r"[a-zA-Z'-]+", input_string)
        return words
```

This function will return us a list of words. We could now calculate other cases.

```python 
    # ...
    def are_words_unique(input_string):
        words = extract_words(input_string)
        
        # Create a set to track unique words
        unique_words = set(words)
        
        # Check if the length of the unique set is the same as the original list
        return len(unique_words) == len(words)

    # ...
    total_cost -= 2 if are_words_unique(input_string)
```

With above we corrected cost if the words are unique.

Now using the ``extract_words(input_string)`` we could calculate word costs. Task is trivial, we have words, so we will get the lengths, use simple
for loop to iterate over the list and calculate the credits.

Next to the palindrome.

```python
    def is_palindrome(words):
        return words == words[::-1]
    ...
    total_cost = 2*(max(1, total_cost))
```

*note*: Ordering is unclear.

We are multiplying the cost by 2 as it is a palindrome, befor the multiplication we are chacking if the credit cost less then 1, and setting it to 1.

Now all we need is to wrap it up into a module and connect to the usage entry.

Time to write an api.

# API

As requested per the task, we need to implement:

> A simple Python API with a single endpoint accessible by making a GET request to /usage that returns the usage data for the current billing period. The endpoint should return a JSON response with the following mentioned above.

Let's use Flask to implement our API, it is small, flexible and fits the task.

Having this in mind we will define a structure like this:

```python
    from flask import Flask, jsonify
    
    app = Flask(__name__)
    
    @app.route('/usage', methods=['GET'])
    def usage():
        # Download data for the period
        # pull the existing reports
        # calculate missing usage
        # return data
        return jsonify({})
    
    if __name__ == '__main__':
        app.run(debug=True)
```

The API is quite simple we are requesting an endpoint with the period start and end. Checking those dates are valid, pulling the data from the endpoint:

```
    https://owpublic.blob.core.windows.net/tech-task/messages/current-period
```

Filtering the entries that fit into the period specified, check those entries have the report IDs,
pull those from this endpoint:

```
    https://owpublic.blob.core.windows.net/tech-task/reports/:id
```

If there are no such reports, then we are calculating the data. Then we return the JSON. Task done.

Let's not rush.

First, let us figure out the period fields.

```python
    # ...
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    # ...
```

We'll use the request from the flask package to get the usage period from the parameters,
to simplify the calculations and comparisons I will use a unix format.

By adding the dates we'll have three cases:
- No dates, we will return all the data from the endpoint
- No start, we will return all up to the end of the period
- No end, same as above but backwards

To pull the data from the messages endpoint we will use a requests package.

Filtering is trivial so I'll skip that.

*Note*: There is the case when no data for a period. We could solve it by returning an empty array or a 404 error

*Note 2*: What to do if end date < start date. We could swap them, but it will be less obvious, or we could return 400 error and let the UI solve this.

That pretty much is about the API, I'd like to leave it as minimalistic as possible, the list of the messages will be processed deeper in the structure.

I think the last thing here is the tests.

We should test the case when the endpoints are unavailable or the dates are wrong.

