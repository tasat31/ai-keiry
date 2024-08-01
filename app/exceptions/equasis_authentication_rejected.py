class EquasisAuthenticationRejected(Exception):
    def __init__(
        self,
        message='Equasis Authentication Rejected',
        error_code='F001',
        imo_no=None
    ):
        if imo_no is None:
            imo_no_message = ''
        else:
            imo_no_message = ': IMO No=%s' % imo_no

        super().__init__(message + imo_no_message)
        self.message = message + imo_no_message
        self.error_code = error_code
