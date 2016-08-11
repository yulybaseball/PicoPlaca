"""
    Main program, in order to use PREDICTOR
"""

from predictor import PPpredictor

predictor = PPpredictor()
message = "Car IS{} allowed to be on the road!"
try:
    plate = input('Enter car plate: ')
    date = input('Enter date (yyyy-mm-dd): ')
    time = input('Enter time (hh:mm): ')
    print message.format("" if predictor.permitted2circulate(plate, date, time) else " NOT")
except Exception, e:
    print str(e)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
