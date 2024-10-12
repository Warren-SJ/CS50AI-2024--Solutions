# Analysis

## Layer 3, Head 1

This attention head seems to be paying attention to the word just before it. This is clear as the most paid attention words are in a diagonal. This is true irrespective of whether the sentence is long or short. This is also true irrespective of the position of the word in the sentence. Layer 3 Head 10 was also similar to this. In both, CLS token is paying colse attention to itself.

Example Sentences:

- Last night, me and my friends went to London to see [MASK].
- I went to the [MASK] to buy some eggs.
- These days, [MASK] is a higly sought after field as it is expected to grow exponentially in the near future.

## Layer 2, Head 7

This attention head seems to be paying attention to the [MASK] and the words around it. Upon trying the first sentecne, it seemed that al words were paying close attention to the mask. However, for the second sentence, only the words from 'go' seem to pay a large attention to it. Focusing on the third sentence, the attention is largely on the first few words until 'highly'. These 3 sentences indicate that the attention is largely on the [MASK] and the words around it. In order to test this, a fourth sentence was used. This was because of the hypothesis that the attention is on the [MASK] and the words around it. This was confirmed as the attention was largely on the [MASK] and the words around it and small for the rest of the words. The reason in the first sentence it seemed all words were paying attention to the [MASK] was because the sentence was small. Since the fourth sentecne is much larger, this was not the case.

Example Sentences:

- The boy jumped [MASK] over the fence
- Every Sunday we make it a habit to go to the [MASK].
- [MASK] is a highly sought after field as it is expected to grow exponentially in the near future.
- In a corner of my neatly arranged [MASK], I sit all by myself reading an interesting novel.
