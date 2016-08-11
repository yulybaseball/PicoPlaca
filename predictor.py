
"""
    Classes to predict the *'Pico y placa'* (Ecuadorian car restriction)
"""

from datetime import datetime

def constant(f):
    """
    Useful to set decorator.
    Used for raising an error when trying to set a value to a variable
    marked as @constant.
    """

    def fset(self, value):
        """ Can not set value to const. """
        raise TypeError('Can not change value using code')

    def fget(self):
        """
        Default method to get property defined with 'constant' decorator.
        """
        return f()

    return property(fget, fset)

class _Const(object):
    """
    Constants to use in *Pico y placa* restrictions.
    """

    @constant
    def MORNING_TIME_RESTRICTION_BEG():
        """ First morning hour for restriction. """
        return '07:00'

    @constant
    def MORNING_TIME_RESTRICTION_END():
        """ Last morning hour for restriction. """
        return '09:30'

    @constant
    def AFTERNOON_TIME_RESTRICTION_BEG():
        """ First afternoon hour for restriction. """
        return '16:00'

    @constant
    def AFTERNOON_TIME_RESTRICTION_END():
        """ Last afternoon hour for restriction. """
        return '19:30'

    @constant
    def DAY_PLATE_RELATION():
        """
        Every dict key is the day of week, and the list associated with it
        contains the plate last digit restricted to be on road for that
        day.
        Following Python built-in library convention, days of week are defined
        this way:
            0: monday
            1: tuesday
            2: wednesday
            3: thursday
            4: friday
            5: saturday
            6: monday
        """
        return {0: [1, 2], 1: [3, 4], 2: [5, 6], 3: [7, 8], 4: [9, 0]}

class PPpredictor():
    """
    Predicts if a car can be on a road.
    In Ecuador, cars are permitted to be on the road according to its last
    plate number. This restriction is called *Pico y placa*.
    Restriction goes from monday to friday, within these time spans:
        - from 07h00 to 09h30
        - from 16h00 to 19h30
    Relation between days of week and last plate number is as follows:
        - monday -> 1 & 2
        - tuesday -> 3 & 4
        - wednesday -> 5 & 6
        - thursday -> 7 & 8
        - friday -> 9 & 0

    TODO: Check validity for parameters, e.g. date, time, plate. Maybe in next
          iteration, ^^.

    """

    @staticmethod
    def _day_of_week(date):
        """
        Returns the day of week for the given date.
        """
        return datetime.strptime(date, "%Y-%m-%d").weekday()

    @staticmethod
    def _plate_belongs2day(plate, date):
        """
        Checks if plate last digit is restricted in a date.
        @param plate: Plate to check if it is restricted.
        @param date: Date to check if plate is restricted in.
        @return: Returns True if @plate last digit is restricted to be
        on road in the day of week corresponding to the @date.
        """
        day_of_week = PPpredictor._day_of_week(date)
        relation = _Const().DAY_PLATE_RELATION
        return (day_of_week in relation and
                int(plate[len(plate) - 1]) in relation[day_of_week])

    @staticmethod
    def _is_restricted_day(date):
        """
        Checks if given date is a restricted day of week.
        """
        return PPpredictor._day_of_week(date) in _Const().DAY_PLATE_RELATION

    @staticmethod
    def _is_restricted_time(time):
        """
        Checks if given time is a restricted one.
        @param time string: Time to check if it is part of the restriction.
        @return: Returns True if time is between restriction time spans. False
        if it is not.
        """
        CONST = _Const()
        return ((CONST.MORNING_TIME_RESTRICTION_BEG <= time <=
                 CONST.MORNING_TIME_RESTRICTION_END) or
                (CONST.AFTERNOON_TIME_RESTRICTION_BEG <= time <=
                 CONST.AFTERNOON_TIME_RESTRICTION_END))

    @staticmethod
    def permitted2circulate(plate, date, time):
        """
        Checks if a car is permitted to circulate.
        @param plate string: plate of the car.
        @param date string: date to check permission in. Should be in the
        style yy-mm-dd.
        @param time string: time to check permission in. Should be in the
        style hh:mm, 24-hour format.
        @return: Returns True if a car with @plate is allowed to be on the road
        at @date, @time. False if it is not allowed.
        """
        pbtd = PPpredictor._plate_belongs2day(plate, date)
        tir = PPpredictor._is_restricted_time(time)
        dair = PPpredictor._is_restricted_day(date)
        return (pbtd and (not dair or not tir)) or not pbtd

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
