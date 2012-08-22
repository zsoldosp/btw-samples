﻿using System;
using System.Collections.Generic;
using System.IO;
using System.Text;

namespace S01E02
{
    class Program
    {
        static void Main(string[] args)
        {
            // Note:  You can push Ctrl+F5 to run this program sample and see the console output

            // Our goal is to allow customers to add & remove shopping items to their product basket
            // so that they can checkout and buy whatever is in the basket when they are done shopping.
            // In the sample below, we will show two possible approaches for achieving that goal:
            // 1)  The traditional approach of calling methods on objects direclty
            // 2)  The messaging approach using message classes that contains the data the remote method needs

            // Note: "Comment" is just a small utility method that helps us write text to the console window
            Comment(@"Let's create a new product basket to hold our shopping items and simply
            add some products to it directly via traditonal BLOCKING method calls.
            ");

            // Create an instance of the ProductBasket class
            // It's AddProduct method takes the following arguments:
            //   a string with the name of a product we want to buy
            //   and a double number indicating the quantity of that item that we want
            // It then stores that item information in its internal _products Dictonary

            var basket = new ProductBasket();

            // Add some products to that shopping basket
            basket.AddProduct("butter", 1);
            basket.AddProduct("pepper", 2);

            // The code above just used normal blocking method calls
            // to add items direclty into the ProductBasket object instance.
            // That works pretty well when the ProductBasket object happens to be
            // running in the same process and thread as the requestor, but not so well when our
            // ProductBasket is running on some other machine or set of machines.
            // In a distributed computing environment like that,
            // a better approach to executing method calls on remote objects like our
            // ProductBasket is to usa a message class with messaging infrastructure.

            // A "message" is just a regular class that you define that will be used to
            // store the required data that the remote object's parameters need you to pass
            // into it as arguments.
            // So from our first example, we know that when we call the ProductBasket's
            // AddProduct method, we need to supply name and quantity arguments to it.
            // We did that directly above but now we are going to use a message class
            // to store the values of the name and quantity arguements for us.
            // The AddProductToBasketMessage is a class defined lower in this Program.cs file
            // that will do exactly that for us.

            Comment(@"
            Now, to add more stuff to the shopping basket via messaging (instead of a
            direct method call), we create an AddProductToBasketMessage to store our name
            and quantity arguments that will be provided to ProductBasket.AddProduct later
            ");

            // creating a new message to hold the arguments of "5 candles" to be addded to the basket
            // looks like Rinat was planning a romantic dinner when he started this sample ;)
            var message = new AddProductToBasketMessage("candles",5);

            Comment(@"Now, since we created that message, we will apply its item contents of:
            ");
            Comment("'" + message + "'" + @" by sending it to the product basket to be handled.
            ");
            ApplyMessage(basket, message);


            Comment(@"
            We don't have to send/apply messages immediately.  We can put messages into 
            some queue and send them later if needed. Let's define more messages to put in a queue:
            ");

            // create more AddProductToBasketMessage's and put them in a queue for processing later
            var queue = new Queue<object>();
            queue.Enqueue(new AddProductToBasketMessage("Chablis wine", 1));
            queue.Enqueue(new AddProductToBasketMessage("shrimps", 10));

            // display each to message on the console
            foreach (var o in queue)
            {
                Comment(" [New Message for Queue is:] * " + o);
            }


            Comment(@"
            This is what temporal decoupling is. Our product basket
            does not need to be available at the same time that we
            create and memorize our messages.

            Now that we feel like it, 
            let's send our messages that we put in the queue to the ProductBasket:
            ");

            while(queue.Count>0)
            {
                ApplyMessage(basket, queue.Dequeue());
            }

            Comment(@"
            Now let's serialize our message to binary form,
            which allows the message object to travel between processes.
            ");

            var serializer = new MessageSerializer(new[] {typeof(AddProductToBasketMessage), typeof(RemoveProductMessage)});

            Comment(@"
            Serialization is a process of recording an object instance
            (which currenly only exists in RAM/memory)
            to a binary representation (which is a set of bytes).
            Serialization is a way that we can save the state of our
            object instances to persistent (non-memory) storage.
            ");

            Comment(@"
            The code will now create another new message for the 'rosmary' product,
            but this time it will serialize it from RAM to disk.
            ");

            using (var mem =new MemoryStream())
            {
                // here is just another message with another product item and quantity
                // we have just decided we are going to serialize this specific one to disk
                var msg = new AddProductToBasketMessage("rosemary", 1);
                serializer.WriteMessage(msg, msg.GetType(), mem);

                Comment(@"
                Let's see how this 'rosmary' message object would look in its binary form:
                ");
                Console.WriteLine(BitConverter.ToString(mem.ToArray()));
                Comment(@"
                And if we tried to open it in a text editor...
                ");
                Console.WriteLine(Encoding.ASCII.GetString(mem.ToArray()));


                Comment(@"
                Note the readable string content with some 'garbled' binary data!
                Now we'll save (persist) the 'rosmary' message to disk, in file 'message.bin'.
                ");

                Comment(@"You can see the message.bin file inside of:

                E002-messaging-basics\sample-csharp\bin\Debug

                If you open it with Notepad, you will see the 'rosmary' message waiting on disk for you.
                ");
                File.WriteAllBytes("message.bin", mem.ToArray());
            }

            Comment(@"
            Let's read the 'rosmary' message we serialzed to file 'message.bin' 
            back into memory.
            The process of reading a serialized object from disk back into memory
            is called deserialization.
            ");
            using (var stream = File.OpenRead("message.bin"))
            {
                var readMessage = serializer.ReadMessage(stream);
                Comment("[Serialized Message was read from disk:] " + readMessage);
                Comment(@"Now let's apply that messaage to the product basket.
                ");
                ApplyMessage(basket, readMessage);
            }

            Comment(@"
            Now you've learned what a message is (just a remote temporally
            decoupled message/method call, that can be persisted and then
            dispatched to the place that handles the request.

            You also learned how to actually serialize a message to a binary form
            and then deserialize it and dispatch it the handler.");

            Comment(@"
            As you can see, you can use messages for passing information
            between machines, telling a story and also persisting.
            
            By the way, let's see what we have aggregated in our product basket so far:
            ");

            foreach (var total in basket.GetProductTotals())
            {
                Console.WriteLine("  {0}: {1}", total.Key, total.Value);
            }

            Comment(@"
            And that is the basics of messaging!
            ");
        }







        static void ApplyMessage(ProductBasket basket, object message)
        {
            // this code accepts the message and actually adds the product to the supplied basket.
            ((dynamic) basket).When((dynamic)message);
        }

        static void Comment(string message)
        {
            // just printing messages nicely
            // and without spaces in the beginning
            Console.ForegroundColor = ConsoleColor.DarkGreen;
            foreach (var line in message.Split(new[] { Environment.NewLine },StringSplitOptions.None))
            {
                Console.WriteLine(line.TrimStart());
            }
            Console.ForegroundColor = ConsoleColor.Gray;
        }

        


        public class ProductBasket
        {
            readonly IDictionary<string, double> _products = new Dictionary<string, double>(); 

            public void AddProduct(string name, double quantity)
            {
                double currentQuantity;
                if (!_products.TryGetValue(name,out currentQuantity))
                {
                    currentQuantity = 0;
                }
                _products[name] = quantity + currentQuantity;

                Console.WriteLine("Shopping Basket said: I added {0} unit(s) of '{1}'", quantity, name);
            }

            public void When(AddProductToBasketMessage toBasketMessage)
            {
                Console.Write("[Message Applied]: ");
                AddProduct(toBasketMessage.Name, toBasketMessage.Quantity);
            }

            public IDictionary<string, double> GetProductTotals()
            {
                return _products;
            } 
        }

        public class AddProductToBasketMessage
        {
            public readonly string Name;
            public readonly double Quantity;

            public AddProductToBasketMessage(string name, double quantity)
            {
                Name = name;
                Quantity = quantity;
            }
            public override string ToString()
            {
                return string.Format("Add {0} {1} to basket", Quantity, Name);
            }
        }
        public class RemoveProductMessage
        {
            public readonly string Name;
            public readonly double Quantity;
            public RemoveProductMessage(string name, double quantity)
            {
                Name = name;
                Quantity = quantity;
            }

            public override string ToString()
            {
                return string.Format("Remove {0} of {1} from basket", Quantity, Name);
            }
        }





    }
}
