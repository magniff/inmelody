import yaml
import watch
import click
import urwid

from libtunes import networking
from libtunes import ui
from libtunes import playback


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
def vktunes(config):
    config_object = Config(yaml.load(config))
    api_object = networking.create_api_handler(config_object)
    getter = networking.AudioGet(api_object)
    _, *audios = getter.call_api()
    records = [playback.AudioRecord(item) for item in audios]
    ui_pl_items = [ui.UIPlaylistItem(record) for record in records]
    pl = ui.UIDefaultMainScreen(ui_pl_items)
    app = ui.UIApplication(pl)
    palette = [
        ('focused', 'white,bold', 'dark red', 'bold'),
        ('unfocused', 'black,standout', 'dark green'),
    ]
    app.run_mainloop(palette)


if __name__ == '__main__':
    vktunes()