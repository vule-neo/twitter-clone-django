from django.apps import AppConfig


class TwitterCompsConfig(AppConfig):
    name = 'twitter_comps'

    def ready(self):
    	import twitter_comps.signals
