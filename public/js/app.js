$(function() {
  $("#query").focus().autocomplete({
    source: function (request, response) {
      $.getJSON("/find_school?term=" + request.term, function (data) {
        response($.map(data.schools, function (value, key) {
          return value;
        }));
      })
    },
    minLength: 3,
    delay: 100,
    select: function( event, ui ) {
      if (ui.item) {
        $.getJSON("/chart/" + ui.item.code, drawVisualization);
      }
    }
  }).data("ui-autocomplete")._renderItem = function( ul, item ) {
    return $("<li>").append("<a>" + item.name + "</a>").appendTo(ul);
  };
});
