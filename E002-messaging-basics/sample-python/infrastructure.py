import pickle # you could import cPickle for performance too

class SimpleSerializer(object):
    # [rinat abdullin]: during the podcast recording we had more complex
    # message serializer in this file (taken from Lokad.CQRS). However,
    # for the first episode it was an overkill...
    def write_message(self, message, message_type, stream): # TODO: unused parameter
        print type(stream), repr(stream)
        pickle.dump(obj=message, file=stream)

    def read_message(self, file):
        return pickle.load(file)
