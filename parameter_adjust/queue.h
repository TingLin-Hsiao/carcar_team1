#ifndef QUEUE_H
#define QUEUE_H

template <typename T, int SIZE>
class Queue {
private:
    T data[SIZE];
    int front;
    int rear;
    int count;

public:
    // Constructor: Initializes the queue
    Queue() {
        front = 0;
        rear = 0;
        count = 0;
    }

    // Check if the queue is empty
    bool isEmpty() {
        return count == 0;
    }

    // Check if the queue is full
    bool isFull() {
        return count == SIZE;
    }

    // Add an item to the queue
    bool enqueue(const T& item) {
        if (isFull()) {
            return false; // Queue is full, cannot enqueue
        }
        data[rear] = item;
        rear = (rear + 1) % SIZE;  // Wrap around if necessary
        count++;
        return true;
    }

    // Remove an item from the queue
    bool dequeue() {
        if (isEmpty()) {
            return -1; // Queue is empty, cannot dequeue
        }
        front = (front + 1) % SIZE; // Wrap around if necessary
        count--;
        return true;
    }
    // Peek at the front item without removing it
    T peek() {
        return data[front];
    }

    // Get the current size of the queue
    int size() {
        return count;
    }
};

#endif
