"""
Please use Python version 3.7+
"""

import csv
from typing import List, Tuple
import timeit


class TweetIndex:
    # Starter code--please override
    def __init__(self):
        self.list_of_tweets = []

    # Starter code--please override
    def process_tweets(self, list_of_timestamps_and_tweets: List[Tuple[str, int]]) -> None:
        """
        process_tweets processes a list of tweets and initializes any data structures needed for
        searching over them.

        :param list_of_timestamps_and_tweets: A list of tuples consisting of a timestamp and a tweet.
        """

        self.unique_words = dict()


        for row in list_of_timestamps_and_tweets:
            timestamp = int(row[0])
            tweet = str(row[1]).lower()

            for word in tweet.split():
                if word not in self.unique_words:
                    self.unique_words[word] = [int(timestamp)]
                elif timestamp not in self.unique_words[word]:
                    self.unique_words[word].append(int(timestamp))

            self.list_of_tweets.append((tweet, timestamp))


    # Starter code--please override
    def search(self, query: str) -> List[Tuple[str, int]]:
        """
        NOTE: Please update this docstring to reflect the updated specification of your search function

        search looks for the most recent tweet (highest timestamp) that contains all words in query.

        :param query: the given query string
        :return: a list of tuples of the form (tweet text, tweet timestamp), ordered by highest timestamp tweets first.
        If no such tweet exists, returns empty list.
        """
        self.stack = list()

        query = query.replace('(', '( ')
        query = query.replace(')', ' )')

        list_of_words = query.lower().split(" ")

        z = list(range(0, len(list_of_tweets)))
        result_tweet, result_timestamp = [], []

        expression_list = []
        expression = False
        and_ =False
        not_ = False

        for word in list_of_words:

            if word == '(':
                expression_list.append(word)
                expression = True
                continue
            elif ')' in word:

                last_3 = expression_list[-3:]

                del expression_list[-3:]
                if last_3[1] == '|':
                    new_list = list(set(last_3[0]) | set(last_3[2]))
                else:
                    new_list = list(set(last_3[0]) & set(last_3[2]))

                expression_list.pop()

                if len(expression_list)==0:
                    expression = False
                    if not self.stack:
                        self.stack.append(new_list)


                    else:
                        if and_:
                            self.stack.append(list(set(self.stack[0]) & set(new_list)))
                        else:
                            self.stack.append(list(set(self.stack[0]) | set(new_list)))
                        self.stack.pop(0)


                else:
                    expression_list.append(new_list)

                continue
            elif word == '|':
                if expression:
                    expression_list.append('|')

                else:
                    if '&' not in list_of_words:
                        pass
                    else:
                        print("Invalid String")
                        return()

            elif word == '&':
                if expression:
                    expression_list.append('&')

                else:
                    and_ = True
            else:
                if '!' in word:
                    word = word[1:]
                    not_ = True

                if word in self.unique_words.keys():
                    if not_:
                        not_ = False
                        if not expression:
                            if len(self.stack) == 0:
                                unique = list(set(z) - set(self.unique_words[word]))
                            else:
                                self.stack.append(list(set(self.stack[0]) - set(self.unique_words[word])))
                                self.stack.pop(0)
                                continue

                        else:
                            if len(expression_list) == 1:
                                unique = list(set(z) - set(self.unique_words[word]))
                            else:
                                unique = list(set(z) - set(self.unique_words[word]))
                                expression_list.append(unique)
                                # self.stack.append(list(set(self.stack[0]) - set(self.unique_words[word])))
                                # self.stack.pop(0)
                                continue


                    else:
                        unique = self.unique_words[word]


                    if expression:
                        expression_list.append(unique)


                    elif and_:
                        self.stack.append(list(set(self.stack[0]) & set(unique)))
                        self.stack.pop(0)
                        and_ = False
                    else:
                        if not self.stack:
                            self.stack.append(unique)
                        else:
                            self.stack.append(list(set(self.stack[0]) | set(unique)))
                            self.stack.pop(0)
                else:
                    if expression:
                        expression_list.append([])

                not_ = False


        if self.stack:
            temp_timestamp = sorted(self.stack.pop(), reverse=True)

            new_list_of_tweets = [x for l in list_of_tweets for x in l]

            for i in temp_timestamp[:5]:
                result_tweet.append(new_list_of_tweets[new_list_of_tweets.index(i) + 1])
                result_timestamp.append(i)
        else:
            result_timestamp.append(-1)
        print([result_tweet, result_timestamp])

        # for tweet, timestamp in self.list_of_tweets:
        #     words_in_tweet = tweet.split(" ")
        #     # print(list_of_words)
        #     # print(words_in_tweet)
        #     tweet_contains_query = True
        #     for word in list_of_words:
        #         if word not in words_in_tweet:
        #             tweet_contains_query = False
        #             break
        #     if tweet_contains_query and timestamp > result_timestamp:
        #         result_tweet, result_timestamp = tweet, timestamp
        # return [(result_tweet, result_timestamp)] if result_timestamp != -1 else []


if __name__ == "__main__":
    # A full list of tweets is available in data/tweets.csv for your use.
    tweet_csv_filename = "../data/tweets.csv"
    list_of_tweets = []
    with open(tweet_csv_filename, "r") as f:
        csv_reader = csv.reader(f, delimiter=",")
        for i, row in enumerate(csv_reader):
            if i == 0:
                # header
                continue
            timestamp = int(row[0])
            tweet = str(row[1])
            list_of_tweets.append((timestamp, tweet))

    ti = TweetIndex()

    # Check for time taken to crate inverted index
    start_time = timeit.default_timer()
    ti.process_tweets(list_of_tweets)
    print("Time for creating inverted index: ",timeit.default_timer()-start_time)
    # Time for creating inverted index:  0.685550200054422

    # Check for single word
    print("----------------------------------------------------------------------")
    start_time = timeit.default_timer()
    ti.search("neeva")
    print("Time taken for: neeva -------", timeit.default_timer()-start_time)
    # [['new way special neeva', 'one his your when neeva get', 'my their by your neeva', 'i up his neeva', 'who from neeva'], [9999, 9998, 9997, 9996, 9995]]
    # Time taken for: neeva ------- 0.002379199955612421

    # Multiple words without any operators
    print("----------------------------------------------------------------------")
    start_time = timeit.default_timer()
    ti.search("get your")
    print("Time taken for: get your -------", timeit.default_timer()-start_time)
    # [['one his your when neeva get', 'my their by your neeva', 'into your go neeva', 'get well neeva', 'get time day neeva'], [9998, 9997, 9994, 9992, 9986]]
    # Time taken for: get your ------- 0.0021250999998301268

    # Check !
    print("----------------------------------------------------------------------")
    start_time = timeit.default_timer()
    ti.search("neeva !special")
    print("Time taken for: neeva !special -------", timeit.default_timer()-start_time)
    # [['one his your when neeva get', 'my their by your neeva', 'i up his neeva', 'who from neeva', 'into your go neeva'], [9998, 9997, 9996, 9995, 9994]]
    # Time taken for: neeva !special ------- 0.0028335999231785536

    # Check &
    print("----------------------------------------------------------------------")
    start_time = timeit.default_timer()
    ti.search("when & your")
    print("Time taken for: when & your -------", timeit.default_timer()-start_time)
    # [['one his your when neeva get', 'your because when neeva get', 'i come your when make neeva who', 'its up your when neeva be know or they but', 'want your when see neeva know look man'], [9998, 9442, 8532, 7311, 7226]]
    # Time taken for: when & your ------- 0.0019176999339833856

    # Multiple |
    print("----------------------------------------------------------------------")
    start_time = timeit.default_timer()
    ti.search("when | your | get")
    print("Time taken for: when | your | get-------", timeit.default_timer()-start_time)
    # [['one his your when neeva get', 'my their by your neeva', 'into your go neeva', 'get well neeva', 'them when here neeva give'], [9998, 9997, 9994, 9992, 9990]]
    # Time taken for: when | your | get------- 0.0026609000051394105

    # To check for invalid string
    print("----------------------------------------------------------------------")
    start_time = timeit.default_timer()
    ti.search("neeva & special | your")
    print("Time taken for: neeva & special | your -------", timeit.default_timer()-start_time)
    # Invalid String
    # Time taken for: neeva & special | your ------- 0.0007287999615073204

    # To check for empty query
    print("----------------------------------------------------------------------")
    start_time = timeit.default_timer()
    ti.search("")
    print("Time taken for:  -------", timeit.default_timer()-start_time)
    # [[], [-1]]
    # Time taken for:  ------- 0.0001362999901175499

    #  To check with expression in query
    print("----------------------------------------------------------------------")
    start_time = timeit.default_timer()
    ti.search("neeva & special & (!than | when) & !your")
    print("Time taken for: neeva & special & (!than | when) & !your -------", timeit.default_timer() - start_time)
    # [['new way special neeva', 'by special in neeva', 'other if that special neeva tell would', 'do special neeva', 'that special those neeva look'], [9999, 9984, 9979, 9975, 9966]]
    # Time taken for: neeva & special & (!than | when) & !your ------- 0.005189299932681024

    # To check for two expressions
    print("----------------------------------------------------------------------")
    start_time = timeit.default_timer()
    ti.search("((special & go) | (speical & your)) & me")
    print("Time taken for: ((special & go) | (speical & your)) & me -------", timeit.default_timer() - start_time)
    # [['out go special me give to neeva first'], [7596]]
    # Time taken for: ((special & go) | (speical & your)) & me ------- 0.0013561000814661384

    # To check for expressions
    print("----------------------------------------------------------------------")
    start_time = timeit.default_timer()
    ti.search("neeva & !special & ((think & go) | (first & this))")
    print("Time taken for: neeva & !special & ((think & go) | (first & this)) -------",
          timeit.default_timer() - start_time)
    # [['up his some find this these neeva first', 'i as go of many them like very neeva think or would', 'think what go neeva', 'for it when this neeva think first', 'go first neeva think give'], [9386, 9257, 9107, 9059, 8469]]
    # Time taken for: neeva & !special & ((think & go) | (first & this)) ------- 0.003401600057259202

    # To check for !word along with & in expression
    print("----------------------------------------------------------------------")
    start_time = timeit.default_timer()
    ti.search("have & (!your & !these)")
    print("Time taken for: have & (!your & !these) -------", timeit.default_timer() - start_time)
    # [['have two by now neeva say', 'have very that neeva', 'have only about well we more now neeva', 'have take me neeva its could', 'have a neeva'], [9987, 9957, 9939, 9928, 9869]]
    # Time taken for: have & (!your & !these) ------- 0.007383199990727007


    # To check output for word not present in csv file
    print("----------------------------------------------------------------------")
    start_time = timeit.default_timer()
    ti.search("bye")
    print("Time taken for: bye -------", timeit.default_timer() - start_time)
    # [[], [-1]]
    # Time taken for: bye ------- 0.00016579998191446066

    # To check for multiple &
    print("----------------------------------------------------------------------")
    start_time = timeit.default_timer()
    ti.search("what & that & say")
    print("Time taken for: what & that & say -------", timeit.default_timer() - start_time)
    # [['what that neeva say look', 'out if what that neeva say'], [9330, 0]]
    # Time taken for: what & that & say ------- 0.0014034999767318368

    # assert ti.search("hello") == ('hello this is also neeva', 15)
    # assert ti.search("hello me") == ('hello not me', 14)
    # assert ti.search("hello bye") == ('hello bye', 3)
    # assert ti.search("hello this bob") == ('hello neeva this is bob', 11)
    # assert ti.search("notinanytweets") == ('', -1)
    print("Success!")