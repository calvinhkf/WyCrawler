import sys

class CustomizeException(Exception):

      def __init__(self, info):
          err = info
          Exception.__init__(self, err)
          # sys.exit(0)
          # self.parameter = parameter
          # self.para_value = para_value