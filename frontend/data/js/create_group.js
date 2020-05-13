import { getCookie } from './load_user.js';

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
      var url_string = window.location;
      var url = new URL(url_string);
      var id = url.searchParams.get('group_id');
      window.location = 'group.html?group_id=' + id;
    }
  };
  xhr.send();
};
