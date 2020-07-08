# Double-Ended-Priority-Queue
A min-max heap implementation for a double ended priority queue with sort stability.
Refer to the medium post [link](https://medium.com/@kiranbaktha2002/min-max-heaps-for-double-ended-priority-queue-b8a6b93997fb) for more details on the implementation and running time.

Original code by Kiran Baktha. Modified by Cameron Allen to add an optional maximum length parameter.

# Usage
<pre>
from depq import DEPQ
queue = DEPQ()
</pre>

## Adding an item with priority
<b>Syntax:</b> queue.push(item, priority=0)

<pre>queue.push('one', 1)  # Adds an item with priority 1</pre>
<pre>queue.push('zero')  # Adds an item with default priority of 0</pre>

<b>Note: </b> Adding an already exisiting item back to the queue updates the priority. <br>
<pre>queue.push('one', 7)  # Updates the previous priority of 'one' with 7</pre>

## Pop the min priority item
<pre> queue.pop_min() </pre>

## Pop the max priority item
<pre> queue.pop_max() </pre>

## Peek the min priority item
<pre> queue.peek_min() </pre>

## Peek the max priority item
<pre> queue.peek_max() </pre>

## Remove a particular item
<pre> queue.remove(item) </pre>

## Check if queue is empty

<pre> queue.empty() </pre>
