'''
- Implement the PageRank algorithm with Spark 
and provide suitable input to test it.

- Given a set of house owners information in the 
format: 
    - OwnerID, HouseID, Zip, Value

- Write a Spark program to compute the average 
house value of each zip code.

- Write a Spark program to compute the inverted 
index of a set of documents. 
More specifically, 
given a set of (DocumentID, text) pairs, output a 
list of (word, (doc1, doc2, …)) pairs.
'''



house_owner_info = {
    'OwnerID': None,
    'HouseID': None,
    'Zip': None,
    'Value': None,
}

documents = ('a.txt', '')
pairs_output = (('dog'), ('a.txt'),)


class DataGenerator:
    def __init__(self) -> None:
        pass

    def gen_house_owner_info(self):
        pass


    def gen_documents(self):
        pass