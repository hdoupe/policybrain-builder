import os.path

import click

from .repository import Repository


class Package(object):
    def __init__(self, name, repo):
        self._name = name
        self._repo = repo
        self._tag = None

    @property
    def name(self):
        return self._name

    @property
    def repo(self):
        return self._repo

    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, value):
        self._tag = value

    def build(self, tag):
        header = click.style(self.name, fg='cyan')

        click.echo("[{}] {}".format(header, click.style("removing", fg='green')))
        self.repo.remove()

        click.echo("[{}] {}".format(header, click.style("cloning", fg='green')))
        self.repo.clone()

        click.echo("[{}] {}".format(header, click.style("fetching", fg='green')))
        self.repo.fetch()

        if tag:
            self.tag = tag
        else:
            self.tag = self.repo.latest_tag()

        click.echo("[{}] {}".format(header, click.style("checking out '{}'".format(self.tag), fg='green')))
        self.repo.checkout(tag=self.tag)

        # self.repo.archive()


def get_packages(names, workdir):
    pkgs = {
        'taxcalc': Package(
            'taxcalc',
            Repository(
                'https://github.com/open-source-economics/Tax-Calculator',
                os.path.join(workdir, 'taxcalc'))),
        'btax': Package(
            'btax',
            Repository(
                'https://github.com/open-source-economics/B-Tax',
                os.path.join(workdir, 'btax'))),
        'ogusa': Package(
            'ogusa',
            Repository(
                'https://github.com/open-source-economics/OG-USA',
                os.path.join(workdir, 'ogusa')))}
    keys = names if names else pkgs.keys()
    return [pkgs[name] for name in keys]
