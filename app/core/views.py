import spotipy
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse


def index(request: HttpRequest) -> HttpResponse:
    cache_handler: spotipy.cache_handler.DjangoSessionCacheHandler = (
        spotipy.cache_handler.DjangoSessionCacheHandler(request)
    )
    auth_manager: spotipy.oauth2.SpotifyOAuth = spotipy.oauth2.SpotifyOAuth(
        scope="user-library-read", cache_handler=cache_handler, show_dialog=True
    )

    if request.GET.get("code", False):
        auth_manager.get_access_token(request.GET.get("code", False))
        return redirect("/")

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        auth_url: str = auth_manager.get_authorize_url()
        return render(
            request, template_name="index.html", context={"auth_url": auth_url}
        )

    spotify = spotipy.Spotify(auth_manager=auth_manager)
    user_data = spotify.me()
    spotify_username = user_data["display_name"]
    tracks = []
    results = spotify.current_user_saved_tracks(limit=1)
    for idx, item in enumerate(results["items"]):
        track = item["track"]
        print(track)
        tracks.append(f"{idx} {track['artists'][0]['name']} – {track['name']}")
    return render(
        request,
        template_name="index.html",
        context={"user": spotify_username, "tracks": tracks},
    )


def sign_out(request: HttpRequest) -> HttpResponse:
    request.session.pop("token_info", None)
    return redirect("index")
