# Roadsign Recognition with a Neural Network

## Process

1. The first neural network was a simple one to make sure everything worked. It had one input layer with relu activation to match the dimensions of the image, one layer to flatten the image and an output layer with a linear activation. from_logits = True was used to calculate the loss and the loss used was the Categorical Cross Entropy Loss. The results of this network were:
   + loss: <span style="color:yellow">1.1641</span>
   + accuracy: <span style="color:yellow">0.8392</span>

    The Adam optimizer was used.

2. The second neural network changed the input layer to a convolutional layer. This layer consisted of 32 filters which the neural netowrk had to learn and the shape of each filter was (3,3).Everything else was kept the same as the previous neural network This netowrk produced the results:
   + loss: <span style="color:yellow">0.9842</span>
   + accuracy: <span style="color:yellow">0.9093</span>

   The results show that using a convolutional neural netowrk has improved the accuracy.

3. The third neural network added a max pooling layer. THe max pooling layer would remove effects due to noise and also, it makes it possible to just know if a feature is present rather than where it is. A maxpooling of (2,2) was used. Additionally, max pooling would downscale the image which would reduce training time. The following were the results of this network.
   + loss: <span style="color:yellow">0.8648</span>
   + accuracy: <span style="color:yellow">0.9070</span>

4. Fourthly, a dense layer of 128 units was added after the flatten layer. This improved the performancs as:
   + loss: <span style="color:yellow">0.3979</span>
   + accuracy: <span style="color:yellow">0.9463</span>

5. Next, the dense layer created above was changed to 256 units. The results were as follows:
   + loss: <span style="color:yellow">0.3449</span>
   + accuracy: <span style="color:yellow">0.9535</span>

6. Next, another convolutional later and max pooling layer were added after the previous convolutional layer and max pooling layer. This too improved the performance of the neural network.
   + loss: <span style="color:yellow">0.2675</span>
   + accuracy: <span style="color:yellow">0.9638</span>

7. The pixel values were regularized by dividing by 255. This caused the following to take place:
   + loss: <span style="color:yellow">0.1049</span>
   + accuracy: <span style="color:yellow">0.9745</span>

8. Finally a dropout layer with dropout probability of 0.5 and a dense layer of size 128 were added just before the output layer. This further changed the performance as:
   + loss: <span style="color:yellow">0.0519</span>
   + accuracy: <span style="color:yellow">0.9882</span>

Since, the performance of the neural network was adequate, this was finalized.


## Other Experimentation

The following were done as eperiments. These were accomplished by modifying the code outside the 2 functions that were asked to be implemented. However, when the assignment was submitted, these parts were changed back to how they were.

1. The number of epochs was changed to 20. These were the results:
   + loss: <span style="color:yellow">0.0467</span>
   + accuracy: <span style="color:yellow">0.9911</span>

2. The number of epochs was changed to 50. These were the results:
   + loss: <span style="color:yellow">0.0348</span>
   + accuracy: <span style="color:yellow">0.9940</span>

3. The image height and width properties were changed from 30 to 60 and the number of epochs was again set to 10. The following results were produced.
   + loss: <span style="color:yellow">0.0548</span>
   + accuracy: <span style="color:yellow">0.9873</span>