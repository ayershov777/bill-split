$(document).ready(function(){
  $('.modal').modal();

  });

  document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.sidenav');
    var instances = M.Sidenav.init(elems, {edge: 'right'});
  });



//   $('#create-group-btn').on('click', function(){
//     $('#create-group-btn').css({ 'display' : 'none'});
//     $('#create-group-form').css({ 'display' : 'inline'});
//   })



// $('.create-group-btn').on('click', function(){
//   $('#create-group-form').css({ 'display' : 'none'});
// })