$(function(){
    $('.menu-btn').on('click', function(){
      $('.menu').toggleClass('is-active');
    });

    $('#pageTop').click(function(){
      $('body,html').animate({
      scrollTop: 0},300);
      return false;
    });
});