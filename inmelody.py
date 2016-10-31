import yaml
import watch
import click

from libtunes import ui
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
    provider.network = provider.Network(Config(yaml.load(config)))
    palette = [
        ('focused', 'black,bold', 'light green', 'bold'),
        ('audio_list_focused', 'white', 'yellow', 'bold'),
        ('unfocused', 'white', 'dark green', 'bold'),
        ('plitem_unfocused', 'white', 'light blue', 'bold'),
        ('background', 'white', 'dark gray', 'bold'),
        ('panel_background', 'white', 'light blue', 'bold'),
    ]
    app = ui.UIDefaultApplication(palette=palette)
    provider.app = provider.App(app)
    provider.playback = provider.Playback()
    provider.ui = provider.UI()
    app.run_mainloop()


if __name__ == '__main__':
    inmelody()
