import yaml
import watch
import click

from combiner import combine


class Config(watch.WatchMe):
    app_id = watch.builtins.InstanceOf(int)
    login = watch.builtins.InstanceOf(str)
    password = watch.builtins.InstanceOf(str)

    def __init__(self, dictionary):
        self.app_id = dictionary['APP_ID']
        self.login = dictionary['LOGIN']
        self.password = "<not set>"


@click.command()
@click.option('-c', '--config', type=click.File(), required=True)
def vktunes(config):
    config_object = Config(yaml.load(config))
    combine(config_object)


if __name__ == '__main__':
    import sys
    sys.argv.extend(["--config", "./config.yml"])
    vktunes()
