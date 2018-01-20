# Lamport's Bakery Algorithm

An implementation of Lamport's Bakery Algorithm. Originally published in 1974:

"A New Solution of Dijkstra's Concurrent Programming Problem"
Communications of the ACM - Aug 1974 17:8

The unique and interesting aspect of this algorithm is that it provides FIFO mutual exclusion without the use of any atomic hardware operations. At the time of publication this had never been done before. While the practical benefit of a software approach is perhaps limited, it is a very clever and interesting algorithm.

The original paper is very accessible (especially so for a Lamport paper) and the proof of correctness is quite intuitive and helps with understanding _why_ the algorithm works. It can be initially confusing why the unsafe read of `choosing[j]` in the lock loop doesn't interfere with the correctness of the algorithm, but indeed it doesn't matter what this read returns, the subsequent operations will still be done correctly.

Original paper:
http://lamport.azurewebsites.net/pubs/bakery.pdf
