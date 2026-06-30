## Week 2, Project

The cleaning rules that was used was similar to the one for *Week 2, Session 2* but required some additional work to also include the *payment_methods* column name from the csv file. The words were separated by an underscore. I used one function, *clean_text*, to handle "regular" text and the payment method text format by using an optional parameter *payment_method* as a flag. One more thing to consider was the *merchant* column, which for certain merchants were all uppercases. I thus made my function to consider that edge case.

Invalid rows was handled by simply raising an error and counting the number of invalid rows to display to the user.

There were a few assumptions that I made. First and foremost, the date column was "normal" and did not seem to need any cleaning up. So I skipped processing it. I interpeted the numbers as float and did not bother to check if it was an integer. From a quick look it seemed like the *currency* column was correctly formatted. However, I still capitalized it.
