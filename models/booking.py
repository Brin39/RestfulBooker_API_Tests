
from .base_model import BaseModel


class BookingDates(BaseModel):
    """Model representing booking dates."""

    def __init__(self, checkin=None, checkout=None):
        self.checkin = checkin
        self.checkout = checkout


class Booking(BaseModel):
    """Model representing a booking."""

    def __init__(
        self,
        firstname=None,
        lastname=None,
        totalprice=None,
        depositpaid=None,
        bookingdates=None,
        additionalneeds=None,
        bookingid=None
    ):
        self.firstname = firstname
        self.lastname = lastname
        self.totalprice = totalprice
        self.depositpaid = depositpaid
        self.bookingdates = bookingdates or BookingDates()
        self.additionalneeds = additionalneeds
        if bookingid is not None:
            self.bookingid = bookingid

    @classmethod
    def from_dict(cls, data):
        """Create Booking instance from dictionary."""
        booking = cls(
            firstname=data.get('firstname'),
            lastname=data.get('lastname'),
            totalprice=data.get('totalprice'),
            depositpaid=data.get('depositpaid'),
            additionalneeds=data.get('additionalneeds'),
            bookingid=data.get('bookingid')
        )

        if 'bookingdates' in data and data['bookingdates']:
            booking_dates = BookingDates(
                checkin=data['bookingdates'].get('checkin'),
                checkout=data['bookingdates'].get('checkout')
            )
            booking.bookingdates = booking_dates

        return booking

    def to_dict(self):
        """Convert booking to dictionary representation."""
        result = {
            'firstname': self.firstname,
            'lastname': self.lastname,
            'totalprice': self.totalprice,
            'depositpaid': self.depositpaid,
            'additionalneeds': self.additionalneeds,
        }

        if hasattr(self, 'bookingdates') and self.bookingdates:
            result['bookingdates'] = {
                'checkin': self.bookingdates.checkin,
                'checkout': self.bookingdates.checkout
            }

        if hasattr(self, 'bookingid') and self.bookingid is not None:
            result['bookingid'] = self.bookingid

        return {k: v for k, v in result.items() if v is not None}