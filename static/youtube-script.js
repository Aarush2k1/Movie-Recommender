var player;
function onYouTubeIframeAPIReady() {
  $("[data-trailer]").each(function () {
    var id = $(this).data("trailer");
    console.log("trialer id is:" + id);
    $(this).html(
      '<iframe id="responsive-player" src="https://www.youtube.com/embed/' +
        id +
        '?enablejsapi=1&autohide=1&showinfo=0&theme=dark" frameborder="0" allowfullscreen></iframe>'
    );

    player = new YT.Player("responsive-player", {
      playerVars: {
        autoplay: 0,
      },
      events: {
        onStateChange: onPlayerStateChange,
      },
    });
  });
}

function onPlayerStateChange(event) {
  switch (event.data) {
    case YT.PlayerState.ENDED:
      player.stopVideo();
      player.seekTo(0);
      $(".card-movie--playing").removeClass("card-movie--playing");
      $("[data-play]").removeClass("is-playing");
      break;
  }
}

$(function () {
  $("#player").hide();
  $("[data-play]").on("click", function () {
    var $card = $(".card-movie");
    if ($card.hasClass("card-movie--playing")) {
      $(this).toggleClass("is-playing");
      $("#movie-image").show();
      $("#player").hide();
      player.pauseVideo();
    } else {
      $(this).toggleClass("is-playing");
      $("#movie-image").hide();
      $("#player").show();
      player.playVideo();
    }
    $card.toggleClass("card-movie--playing");
  });
});
