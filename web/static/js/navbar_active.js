$(document).ready(function () {

// every new window has nav li plain without active class
// nav links reload whole page
// everytime I set active the corresponding nav link

var my = $(".nav li a[href$="+window.location.pathname.substring(1)+"]");
my.parent().addClass('active');
});
