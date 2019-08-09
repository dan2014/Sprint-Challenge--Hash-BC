#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_remove,
                        hash_table_retrieve,
                        hash_table_resize)


class Ticket:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination


def reconstruct_trip(tickets, length):
    ht = HashTable(length)
    route = [None] * length

    for i in tickets:
        hash_table_insert(ht,i.source,i.destination)

    key = "NONE"
    for j,_ in enumerate(tickets):
        route[j] = key = hash_table_retrieve(ht,key)
        print(key)

    return route

# tickets = [
#   Ticket("PIT", "ORD" ),
#   Ticket("XNA", "CID" ),
#   Ticket("SFO", "BHM" ),
#   Ticket("FLG", "XNA" ),
#   Ticket("NONE", "LAX" ),
#   Ticket("LAX", "SFO" ),
#   Ticket("CID", "SLC" ),
#   Ticket("ORD", "NONE" ),
#   Ticket("SLC", "PIT" ),
#   Ticket("BHM", "FLG" )
# ]

# reconstruct_trip(tickets, len(tickets))