import infrastructure
import os
from collections import deque

# using System;
# using System.Collections.Generic;
# using System.IO;
# using System.Text;
# using System.Reflection;
# 
# namespace E002
# {
#     class Program
#     {

def apply_message(basket, message):
    method_to_call = 'when_%s' % type(message).__name__.lower() # TODO: should make this separate by underscores
    assert hasattr(basket, method_to_call), '%s has no method called %s' % (type(basket), method_to_call)
    getattr(basket, method_to_call)(message)

def main():
    readme_file_name = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', '..', 'ReadMe.md')
    )
    # TODO: should I create a separate readme file for python?
    with open(readme_file_name, 'r') as f:
        _print(f.read())
    # Note:  You can push Ctrl+F5 to run this program sample and see the console output
    # Our goal is to allow customers to add & remove shopping items to their product basket
    # so that they can checkout and buy whatever is in the basket when they are done shopping.
    # In the sample below, we will show two possible approaches for achieving that goal:
    # 1)  The traditional approach of calling methods on objects direclty
    # 2)  The messaging approach using message classes that contains the data the remote method needs
    # 
    # Note: "_print" is just a small utility method that helps us write text to the console window
    _print("""
        Let's create a new product basket to hold our shopping items and simply
        add some products to it directly via traditonal BLOCKING method calls.
    """);

    # Create an instance of the ProductBasket class
    # Its AddProduct method takes the following arguments:
    #   a string with the name of a product we want to buy
    #   and a double number indicating the quantity of that item that we want
    # It then stores that item information in its internal _products Dictonary

    basket = ProductBasket()

    # Add some products to that shopping basket
    basket.add_product('buter', 1)
    basket.add_product('pepper', 2)

    # The code above just used normal blocking method calls
    # to add items direclty into the ProductBasket object instance.
    # That works pretty well when the ProductBasket object happens to be
    # running in the same process and thread as the requestor, but not so well when our
    # ProductBasket is running on some other machine or set of machines.
    # In a distributed computing environment like that,
    # a better approach to executing method calls on remote objects like our
    # ProductBasket is to use a message class with messaging infrastructure.

    # A "message" is just a regular class that you define that will be used to
    # store the required data that the remote object's parameters need you to pass
    # into it as arguments.
    # So from our first example, we know that when we call the ProductBasket's
    # AddProduct method, we need to supply name and quantity arguments to it.
    # We did that directly above but now we are going to use a message class
    # to store the values of the name and quantity arguements for us.
    # The AddProductToBasketMessage is a class defined lower in this Program.cs file
    # that will do exactly that for us.
 
    _print("""
        Now, to add more stuff to the shopping basket via messaging (instead of a
        direct method call), we create an AddProductToBasketMessage to store our name
        and quantity arguments that will be provided to ProductBasket.AddProduct later
    """);
 
    # creating a new message to hold the arguments of "5 candles" to be addded to the basket
    # looks like Rinat was planning a romantic dinner when he started this sample ;)
    message = AddProductToBasketMessage("candles", 5)

    _print(u"""
        Now, since we created that message, we will apply its item contents of:
        '%s'
        by sending it to the product basket to be handled.
    """ % message)

    apply_message(basket, message)
    _print("""
        We don't have to send/apply messages immediately.  We can put messages into 
        some queue and send them later if needed. 
        
        Let's define more messages to put in a queue:
    """)
    # create more AddProductToBasketMessage's and put them in a queue for processing later
    queue = deque([])
    queue.append(AddProductToBasketMessage("Chablis wine", 1))
    queue.append(AddProductToBasketMessage("shrimps", 10))
    for enqueuedMessage in queue:
        print u" [Message in Queue is:] * %s" % enqueuedMessage
# 
# 
#             Print(@"
#             This is what temporal decoupling is. Our product basket does not 
#             need to be available at the same time that we create and memorize
#             our messages. This will be extremely important, when we get to 
#             building systems that balance load and can deal with failures.
# 
#             Now that we feel like it, let's send our messages that we put in the
#             queue to the ProductBasket:
#             ");
# 
#             while(queue.Count>0)
#             {
#                 ApplyMessage(basket, queue.Dequeue());
#             }
# 
#             Print(@"
#             Now let's serialize our message to binary form,
#             which allows the message object to travel between processes.
#             ");
# 
    # Note: In the podcast we mentioned "MessageSerializer" as the code doing
    # the serialization.  That was replaced below with "SimpleNetSerializer"
    # to do the same thing in a simpler way to remove complexity from this sample.
# 
#             var serializer = new SimpleNetSerializer();
# 
# 
#             Print(@"
#             Serialization is a process of recording an object instance
#             (which currenly only exists in RAM/memory)
#             to a binary representation (which is a set of bytes).
#             Serialization is a way that we can save the state of our
#             object instances to persistent (non-memory) storage.
# 
# 
#             The code will now create another new message for the 'rosmary' product,
#             but this time it will serialize it from RAM to disk.
#             ");
# 
    # here is just another message with another product item and quantity
    # we have just decided we are going to serialize this specific one to disk
#             var msg = new AddProductToBasketMessage("rosemary", 1);
# 
    # this operation will use memory stream to convert message
    # to in-memory array of bytes, which we will operate later
#             byte[] bytes;
#             using (var stream = new MemoryStream())
#             {
#                 serializer.WriteMessage(msg, msg.GetType(), stream);
#                 bytes = stream.ToArray();
#             }
# 
#             Print(@"
#             Let's see how this 'rosmary' message object would look in its binary form:
#             ");
#             Console.WriteLine(BitConverter.ToString(bytes).Replace("-",""));
#             Print(@"
#             And if we tried to open it in a text editor...
#             ");
#             Console.WriteLine(Encoding.ASCII.GetString(bytes));
# 
#             Print(@"
#             Note the readable string content with some 'garbled' binary data!
#             Now we'll save (persist) the 'rosmary' message to disk, in file 'message.bin'.
#                 
#             You can see the message.bin file inside of:
# 
#             '" + Path.GetFullPath("message.bin") + @"'
# 
#             If you open it with Notepad, you will see the 'rosmary' message waiting on disk for you.
#             ");
#             File.WriteAllBytes("message.bin", bytes);
# 
# 
#             Print(@"
#             Let's read the 'rosmary' message we serialized to file 'message.bin' back into memory.
# 
#             The process of reading a serialized object from byte array back into intance in memory 
#             is called deserialization.
#             ");
#             using (var stream = File.OpenRead("message.bin"))
#             {
#                 var readMessage = serializer.ReadMessage(stream);
#                 Print("[Serialized Message was read from disk:] " + readMessage);
#                 Print(@"Now let's apply that messaage to the product basket.
#                 ");
#                 ApplyMessage(basket, readMessage);
#             }
# 
#             Print(@"
#             Now you've learned what a message is (just a remote temporally
#             decoupled message/method call, that can be persisted and then
#             dispatched to the place that handles the request.
# 
#             You also learned how to actually serialize a message to a binary form
#             and then deserialize it and dispatch it the handler.");
# 
#             Print(@"
#             As you can see, you can use messages for passing information
#             between machines, telling a story and also persisting.
#             
#             By the way, let's see what we have aggregated in our product basket so far:
#             ");
# 
#             foreach (var total in basket.GetProductTotals())
#             {
#                 Console.WriteLine("  {0}: {1}", total.Key, total.Value);
#             }
# 
#             Print(@"
#             And that is the basics of messaging!
# 
#             Stay tuned for more episodes and samples!
# 
# 
#             # Home work assignment.
# 
#             * For C# developers - implement 'RemoveProductFromBasket'
#             * For non-C# developers - implement this code in your favorite platform.
# 
#             NB: Don't hesitate to ask questions, if you get any.
#             ");
#         }
# 

def _print(message):
    """
        Prints messages nicely, without spaces in the beginning
    """
    """
        >>> import curses
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
          File "C:\lib\Python\3.2-x86\lib\curses\__init__.py", line 15, in <module>
            from _curses import *
        ImportError: No module named _curses    
    """
    for line in message.splitlines():
        trimmed = line.lstrip()
        if trimmed.startswith('#'):
            pass # TODO: Console.ForegroundColor = ConsoleColor.DarkRed;
        elif any(trimmed.startswith(pattern) for pattern in ['*', '- ']):
            pass # TODO Console.ForegroundColor = ConsoleColor.DarkBlue;
        else:
            pass # TODO: Console.ForegroundColor = ConsoleColor.DarkGreen;
        print trimmed
        pass # TODO: Console.ForegroundColor = oldColor;
# 
#         
# 
# 
class ProductBasket(object):
    def __init__(self):
        self._products = {}

    def add_product(self, name, quantity): # TODO: does it really have to be double like the C# prog says?
        current_quantity = self._products.get(name, 0)
        self._products[name] = current_quantity + quantity 
        print '%(object)s said: I added %(quantity).2f unit(s) of %(product_name)s' % dict(
                object = type(self).__name__,
                quantity = quantity,
                product_name = name
            )

    def when_addproducttobasketmessage(self, message):
        print "[Message Applied]: "
        self.add_product(message.name, message.quantity)
# 
#             public void When(AddProductToBasketMessage toBasketMessage)
#             {
#                 Console.Write(
#                 AddProduct(toBasketMessage.Name, toBasketMessage.Quantity);
#             }
# 
#             public IDictionary<string, double> GetProductTotals()
#             {
#                 return _products;
#             } 
#         }

class AddProductToBasketMessage(object):
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

    def __unicode__(self):
        return 'Add %(quantity).2f %(product_name)s to basket' % dict(quantity=self.quantity, product_name=self.name)

if __name__ == '__main__':
    main()
