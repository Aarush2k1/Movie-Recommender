var reviews_list;

function load_details(my_api_key, title) {
  $.ajax({
    type: "GET",
    url:
      "https://api.themoviedb.org/3/search/movie?api_key=" +
      my_api_key +
      "&query=" +
      title,

    success: function (movie) {
      if (movie.results.length < 1) {
        $(".results").css("display", "none");
      } else {
        $(".results").delay(1000).css("display", "block");
        var movie_id = movie.results[0].id;
        var movie_title = movie.results[0].original_title;
        console.log(movie_id);
        // movie_recs(movie_title, movie_id, my_api_key);
      }
    },
    error: function () {
      alert("Invalid Request");
      $("#loader").delay(500).fadeOut();
    },
  });
}
function load_movie_details(api_key) {
  // Fetching all info of movie
  $.ajax();
  fetch(
    `https://api.themoviedb.org/3/movie/${movie_id}?api_key=385371f8e8338ab21088dcf461296d86&language=en-US`
  )
    .then((response) => response.json())
    .then((data) => {
      if (data) {
        const movie_overview = data["overview"];
        document.getElementById("movie_overview").innerHTML = movie_overview;
        const movie_votes = data["vote_average"];
        document.getElementById("movie_votes").innerHTML = movie_votes;
        const movie_image_url =
          "url('https://image.tmdb.org/t/p/original" +
          data["backdrop_path"] +
          "')";
        document.getElementById("main-movie-image").style.backgroundImage =
          movie_image_url;
      } else {
        alert("Movie not found");
      }
    });
  // Get trailer key
  fetch(
    `https://api.themoviedb.org/3/movie/${movie_id}/videos?api_key=385371f8e8338ab21088dcf461296d86`
  )
    .then((response) => response.json())
    .then((data) => {
      console.log(data.results[data.results.length - 1].key);
      if (data.results.length) {
        var video_key = data.results[data.results.length - 1].key;
        document
          .getElementById("player")
          .setAttribute("data-trailer", video_key);
      } else {
        alert("Trailer not found");
      }
    });
  // Get reviews
  fetch(
    `https://api.themoviedb.org/3/movie/${movie_id}/reviews?api_key=385371f8e8338ab21088dcf461296d86&language=en-US&page=1`
  )
    .then((response) => response.json())
    .then((data) => {
      reviews_list = data.results;
      var table = document.getElementById("reviews-table");
      console.log(reviews_list.length);
      if (reviews_list.length > 4) {
        for (var i = 0; i < 3; i++) {
          var div = document.createElement("div");
          div.innerHTML = i + 1 + "). " + reviews_list[i].content + " ";
          table.append(div);
        }
      } else {
        for (var i = 0; i < reviews_list.length; i++) {
          var div = document.createElement("div");
          div.innerHTML = i + 1 + "). " + reviews_list[i].content + " ";
          table.append(div);
        }
      }
    });
}
var details = {
  reviews: reviews_list,
};

$(function () {
  // $("#submit-btn").on("click", function () {
  //   var api_key = "385371f8e8338ab21088dcf461296d86";
  //   var title = $(".title").val();
  //   if (title == "") {
  //     $(".results").css("display", "none");
  //     console.log("no title");
  //   } else {
  //     console.log(title);
  //     load_details(api_key, title);
  //   }
  // });
});
