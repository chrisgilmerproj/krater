$('.btn').click( function() {
  var star = $(this).attr('val');
  var id = $(this).parent().attr('val');
  $.post('../star/', {star: star, id: id});
})
