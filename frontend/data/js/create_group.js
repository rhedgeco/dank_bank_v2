function getCookie(cname) {
  var name = cname + '=';
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for (var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) === ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) === 0) {
      return c.substring(name.length, c.length);
    }
  }
  return 0;
}

//API call
var btn2 = document.getElementById('create_form');

btn2.onclick = function () {
  let xhr = new XMLHttpRequest();
  xhr.open(
    'POST',
    'api/groups?session=' +
      getCookie('session_id') +
      '&group_name=' +
      document.getElementById('group_name').value
  );
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.onload = function () {
    if (xhr.status === 200) {
      console.log('group successfully created');
    }
  };
  xhr.send();
};
