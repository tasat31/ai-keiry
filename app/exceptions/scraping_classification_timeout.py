class ScrapingClassificationTimeout(Exception):
    def __init__(
        self,
        message='Timeout when scraping classification site',
        error_code='F003',
        imo_no=None
    ):
        if imo_no is None:
            imo_no_message = ''
        else:
            imo_no_message = ': IMO No=%s' % imo_no

        super().__init__(message + imo_no_message)
        self.message = message + imo_no_message
        self.error_code = error_code
