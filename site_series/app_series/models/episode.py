import json
import requests
import site_series.settings as settings
from django.db import models

from app_series.models.season import Season


class EpisodeManager(models.Manager):
    def create_episode_from_args(self, season, episode_nb, **kwargs):
        episode = Episode.objects.filter(season=season, episode_nb=episode_nb)
        if len(episode) == 0:
            episode = Episode.objects.create(season=season, episode_nb=episode_nb, **kwargs)
            episode.save()
        else:
            episode.update(**kwargs)
            episode = episode.first()
        return episode

    def create_episode(self, tmdb_id, season_nb, episode_nb):
        url = settings.TMDB_API_URL + "tv/" + str(tmdb_id) + "/season/" + str(season_nb) + "/episode/" + str(episode_nb)
        content = json.loads(requests.get(url, params={"api_key": settings.TMDB_API_KEY}).content.decode())

        episode = self.create_episode_from_args(
            season=Season.objects.create_season(tmdb_id=tmdb_id, season_nb=season_nb),
            episode_nb=episode_nb,
            title=content["name"],
            overview=content["overview"],
            vote_average=content["vote_average"]
        )
        return episode

class Episode(models.Model):
    """Definition of the class Episode, it contains the following attributes:
                    - id of the TvShow
                    - episode_nb: episode number
                    - id of the episode
                    - name : episode name
                    - overview : the description of the episode
                    - broadcast_date : the release date of the episode
                    - an average score for the episode"""
    season = models.ForeignKey('Season', default=0)
    episode_nb = models.IntegerField(default=0)
    title = models.CharField(max_length=100, null=True)
    overview = models.CharField(max_length=1000, null=True)
    vote_average = models.IntegerField(default=0)

    objects = EpisodeManager()