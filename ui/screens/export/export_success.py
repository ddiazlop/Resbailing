from ui.utils.superclasses.RelativeLayoutScreen import RelativeLayoutScreen


class ExportSuccessScreen(RelativeLayoutScreen):
    def __init__(self, main_app, **kwargs):
        super().__init__(main_app, 'ui/screens/export/export_success.kv', **kwargs)
