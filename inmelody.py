import yaml
import watch
import click

from libtunes import networking
from libtunes import ui
from libtunes import playback
from libtunes import provider


class Config(watch.WatchMe):
    app_id = watch.builtins.InstanceOf(int)
    login = watch.builtins.InstanceOf(str)
    password = watch.builtins.InstanceOf(str)

    def __init__(self, dictionary):
        self.app_id = dictionary.get('APP_ID')
        self.login = dictionary.get('LOGIN')
        self.password = dictionary.get('PASSWORD')


@click.command()
@click.option('-c', '--config', type=click.File(), required=True)
def inmelody(config):
    provider.handle = provider.configure(Config(yaml.load(config)))
    app = ui.UIDefaultApplication()
    palette = [
        ('focused', 'black,bold', 'light green', 'bold'),
        ('unfocused', 'white', 'dark green', 'bold'),
        ('background', 'white', 'dark gray', 'bold'),
        ('panel_background', 'white', 'light blue', 'bold'),
    ]
    app.run_mainloop(palette)


if __name__ == '__main__':
    inmelody()
